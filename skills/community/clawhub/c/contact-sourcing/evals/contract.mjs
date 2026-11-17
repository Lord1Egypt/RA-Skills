import assert from "node:assert/strict";
import { readFileSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { compile, resetRegistry, resources } from "@cargo-ai/cdk";

// The CLI separates infra from the copied skill. Locate either layout without
// accidentally importing a historical or sibling implementation.
const localInfra = fileURLToPath(new URL("../infra/index.ts", import.meta.url));
const findConsumerInfra = () => {
  for (
    let directory = dirname(fileURLToPath(import.meta.url));
    ;
    directory = dirname(directory)
  ) {
    const file = join(directory, "infra/contact-sourcing/index.ts");
    if (existsSync(file)) return file;
    if (dirname(directory) === directory) break;
  }
  return null;
};
const infraPath = process.env.CONTACT_SOURCING_INFRA
  ? resolve(process.env.CONTACT_SOURCING_INFRA)
  : existsSync(localInfra)
    ? localInfra
    : findConsumerInfra();
assert.ok(
  infraPath,
  "Set CONTACT_SOURCING_INFRA to the adapted index.ts if using a custom layout",
);
resetRegistry();
const {
  configuration,
  buildContactSourcing,
  qualificationSchema,
  qualificationAgentSettings,
} = await import(pathToFileURL(infraPath).href);
// The standalone example owns exactly these resources. A consumer can import
// compatible existing handles; their unrelated resources are reviewed in its
// project plan, not mistaken for dependencies introduced by this tool.
if (infraPath === localInfra)
  assert.deepEqual(
    resources()
      .map((r) => r.kind)
      .sort(),
    configuration.qualificationBackend === "agent"
      ? [
          "agent",
          "connector",
          "connector",
          "connector",
          "folder",
          "folder",
          "tool",
        ]
      : ["connector", "connector", "connector", "folder", "tool"],
  );
const deployed = resources().find((r) => r.id === "tool:contact_sourcing");
assert.ok(deployed);
assert.equal(deployed.spec.triggers?.length || 0, 0);
assert.deepEqual(
  deployed.spec.nodes,
  buildContactSourcing(configuration).nodes,
  "the deployed tool must use the tested builder",
);

// Exercise the emitted graph, including nested groups, expressions, actual scripts,
// failure successors and end-variable mappings. Only external calls are mocked.
// This is a contract harness, not a simulation of Cargo's remote engine.
const evaluate = (value, nodes, parentNodes) => {
  if (
    value &&
    typeof value === "object" &&
    value.kind === "templateExpression"
  ) {
    const code = value.expression;
    const exact = code.match(/^\{\{([\s\S]*)\}\}$/);
    const run = (source) =>
      new Function("nodes", "parentNodes", `return (${source});`)(
        nodes,
        parentNodes,
      );
    return exact
      ? run(exact[1])
      : code.replace(/\{\{(.*?)\}\}/g, (_, source) => String(run(source)));
  }
  if (Array.isArray(value))
    return value.map((v) => evaluate(v, nodes, parentNodes));
  if (value && typeof value === "object")
    return Object.fromEntries(
      Object.entries(value).map(([key, v]) => [
        key,
        evaluate(v, nodes, parentNodes),
      ]),
    );
  return value;
};
const walk = (nodes) =>
  nodes.flatMap((n) => [n, ...walk(n.config._nodes || [])]);
const validateGraph = (nodes) => {
  const ids = new Set(nodes.map((n) => n.uuid));
  assert.equal(ids.size, nodes.length);
  assert.equal(nodes.filter((n) => n.slug === "start").length, 1);
  assert.equal(nodes.filter((n) => n.actionSlug === "end").length, 1);
  for (const n of nodes) {
    assert.match(
      n.uuid,
      /^[\da-f]{8}-[\da-f]{4}-4[\da-f]{3}-[89ab][\da-f]{3}-[\da-f]{12}$/,
    );
    for (const uuid of n.childrenUuids)
      assert.ok(ids.has(uuid), `${n.slug}: dangling child`);
    if (n.fallbackChildUuid) assert.ok(ids.has(n.fallbackChildUuid));
    assert.equal(
      n.childrenUuids.length,
      n.actionSlug === "end" ? 0 : n.actionSlug === "branch" ? 2 : 1,
    );
    if (n.config._nodes) validateGraph(n.config._nodes);
  }
  const reachable = new Set();
  const visit = (id) => {
    if (reachable.has(id)) return;
    reachable.add(id);
    const n = nodes.find((n) => n.uuid === id);
    n.childrenUuids.forEach(visit);
  };
  visit(nodes.find((n) => n.slug === "start").uuid);
  assert.equal(reachable.size, nodes.length, "no unused nodes");
};
const runGraph = async (
  graph,
  input,
  external,
  parentNodes = {},
  reverseGroups = true,
) => {
  const nodes = { start: input };
  let current = graph.find((n) => n.slug === "start");
  for (let steps = 0; steps < 100; steps++) {
    let next = current.childrenUuids[0];
    const cfg = current.config;
    if (current.kind !== "native") {
      const computed = evaluate(cfg, nodes, parentNodes);
      try {
        nodes[current.slug] = await external(
          current,
          computed,
          nodes,
          parentNodes,
        );
      } catch (error) {
        if (!current.fallbackOnFailure) throw error;
        next = current.fallbackChildUuid;
      }
    } else if (current.actionSlug === "branch")
      next =
        current.childrenUuids[
          evaluate(cfg.condition, nodes, parentNodes) ? 0 : 1
        ];
    else if (current.actionSlug === "script")
      nodes[current.slug] = {
        result: new Function("nodes", "parentNodes", cfg.script)(
          nodes,
          parentNodes,
        ),
      };
    else if (["variables", "end"].includes(current.actionSlug)) {
      const result = Object.fromEntries(
        cfg.variables.map((v) => [
          v.name,
          evaluate(v.value, nodes, parentNodes),
        ]),
      );
      if (current.actionSlug === "end") return result;
      nodes[current.slug] = result;
    } else if (current.actionSlug === "group") {
      const items = evaluate(cfg.items, nodes, parentNodes);
      const results = await Promise.all(
        items.map(async (item) => {
          try {
            return await runGraph(
              cfg._nodes,
              item,
              external,
              nodes,
              reverseGroups,
            );
          } catch (error) {
            if (cfg.failOnItemFailure) throw error;
            return null;
          }
        }),
      );
      nodes[current.slug] = reverseGroups ? results.reverse() : results;
    } else
      assert.equal(
        current.actionSlug,
        "start",
        `unsupported native node ${current.actionSlug}`,
      );
    current = graph.find((n) => n.uuid === next);
    assert.ok(current, "the graph must reach its end");
  }
  assert.fail("graph did not terminate");
};

// Fictional people only. The titles deliberately do not determine the fixture score.
const candidate = (id, title = "Planning Engineer") => ({
  linkedin_profile_id: Number(id),
  linkedin_profile_url: `https://www.linkedin.com/in/fictional-${id}`,
  full_name: `Fictional Person ${id}`,
  job_title: title,
});
const profile = (id, overrides = {}) => ({
  profile_id: id,
  linkedin_url: `https://www.linkedin.com/in/fictional-${id}`,
  full_name: `Fictional Person ${id}`,
  first_name: "Fictional",
  last_name: `Person ${id}`,
  job_title: "Planning Engineer",
  company: "Example Infrastructure",
  company_domain: "infrastructure.example",
  about: "Owns P6 capital-project schedules and schedule-risk analysis.",
  experiences: [
    {
      company: "Example Infrastructure",
      company_id: "123",
      title: "Planning Engineer",
      description: "Owns P6 capital-project schedules.",
      is_current: true,
    },
  ],
  ...overrides,
});
const verdict = (score = 8, overrides = {}) => ({
  status: "qualified",
  score,
  matchedPersona: configuration.personaIds[0],
  buyingRole: "end_user",
  employment: "current",
  explanation:
    "Direct responsibility for project schedules; end-user role is an inference.",
  evidence: ["Owns P6 capital-project schedules."],
  flags: [],
  ...overrides,
});
const company = {
  company_id: "123",
  linkedin_url: "https://www.linkedin.com/company/example-infrastructure",
  domain: "infrastructure.example",
  company_name: "Example Infrastructure",
};
const emailPolicy = {
  email: true,
  phone: false,
  emailToolUuid: "52000000-0000-4000-8000-000000000001",
  emailVerificationConnectorUuid: "52000000-0000-4000-8000-000000000003",
};
const phonePolicy = {
  email: false,
  phone: true,
  phoneToolUuid: "52000000-0000-4000-8000-000000000002",
};
const enrichmentPolicies = [
  { email: false, phone: false },
  emailPolicy,
  phonePolicy,
  { ...emailPolicy, phone: true, phoneToolUuid: phonePolicy.phoneToolUuid },
];
const agentFixtureUuid = "52000000-0000-4000-8000-000000000004";
const qualificationPolicies = [
  {
    qualificationBackend: "openai_action",
    qualificationProvider: "openAi",
    qualificationModel: "gpt-5-mini",
  },
  {
    qualificationBackend: "agent",
    qualificationProvider: "openAi",
    qualificationModel: "gpt-5-mini",
  },
  // Fixture identifier only; consumers resolve a real supported model at setup.
  {
    qualificationBackend: "agent",
    qualificationProvider: "anthropic",
    qualificationModel: "claude-fixture",
  },
];

const exercise = async ({
  policy = {},
  input = { companyId: "123" },
  rows = [candidate("1")],
  profiles = {},
  answers = {},
  failure = [],
  email = {},
  phone = {},
  verification = {},
  reverseGroups = true,
} = {}) => {
  const config = {
    ...configuration,
    inputMode: "id",
    email: false,
    phone: false,
    searchLimit: 50,
    topN: null,
    minimumScore: null,
    ...qualificationPolicies[0],
    ...policy,
  };
  const graph = buildContactSourcing(config, agentFixtureUuid);
  validateGraph(graph.nodes);
  const calls = [];
  const result = await runGraph(
    graph.nodes,
    input,
    async (node, data, local, parent) => {
      calls.push({ slug: node.slug, data, identity: local.start.identity });
      if (
        failure.includes(node.slug) ||
        failure.includes(node.slug + ":" + local.start.identity)
      )
        throw new Error("Fictional provider failure");
      if (node.slug.startsWith("resolve_"))
        return typeof profiles.company === "function"
          ? profiles.company(data)
          : (profiles.company ?? company);
      if (node.slug === "search") {
        assert.deepEqual(
          data.company.currentCompanyIds,
          ["123"],
          "every search must have a resolved current-company scope",
        );
        return rows;
      }
      if (node.slug === "profile") {
        const id = local.start.personId;
        return Object.hasOwn(profiles, id) ? profiles[id] : profile(id);
      }
      if (node.slug === "qualify") {
        if (config.qualificationBackend === "agent") {
          assert.equal(node.kind, "agent");
          assert.equal(node.agentUuid, agentFixtureUuid);
          assert.equal(data.output.type, "jsonSchema");
        } else {
          assert.equal(node.kind, "connector");
          assert.equal(data.model, config.qualificationModel);
        }
        assert.deepEqual(data.output.jsonSchema, qualificationSchema);
        assert.ok(data.prompt.includes(config.sellerCriteria));
        assert.ok(data.prompt.includes(JSON.stringify(local.profile)));
        if (input.accountContext)
          assert.ok(data.prompt.includes(JSON.stringify(input.accountContext)));
        const id = local.start.personId;
        return { answer: Object.hasOwn(answers, id) ? answers[id] : verdict() };
      }
      if (node.slug === "email_lookup")
        return Object.hasOwn(email, local.start.identity)
          ? email[local.start.identity]
          : { email: "fictional@infrastructure.example" };
      if (node.slug === "verify_email")
        return (
          verification[local.start.identity] ?? {
            email: data.email,
            email_status: "valid",
          }
        );
      if (node.slug === "phone_lookup")
        return Object.hasOwn(phone, local.start.identity)
          ? phone[local.start.identity]
          : { phone: "+12025550123" };
      assert.fail(`unexpected external call ${node.slug}`);
    },
    {},
    reverseGroups,
  );
  return { result, calls, graph };
};
let checks = 0;
const check = async (name, fn) => {
  await fn();
  checks++;
  console.log(`ok: ${name}`);
};

await check("the selected installation configuration executes", async () => {
  const planned = await compile({ nodes: resources() });
  assert.deepEqual(planned.errors, [], "the selected resources must compile");
  const agent = resources().find(
    (r) => r.id === "agent:contact_sourcing_qualifier",
  );
  if (agent) {
    assert.equal(
      agent.spec.languageModelSlug,
      configuration.qualificationModel,
    );
    assert.deepEqual(agent.spec.output.jsonSchema, qualificationSchema);
    assert.equal(agent.spec.harnessSlug, undefined);
    assert.equal(agent.spec.maxSteps, 1);
    assert.equal(
      resources().find(
        (r) => r.id === "connector:contact_sourcing_qualification",
      ).spec.integrationSlug,
      configuration.qualificationProvider,
    );
  }
  const inputs = {
    id: { companyId: "123" },
    url: { linkedinCompanyUrl: company.linkedin_url },
    domain: { domain: company.domain },
    multiple: { companyId: "123" },
  };
  const { result } = await exercise({
    policy: configuration,
    input: inputs[configuration.inputMode],
  });
  const expected =
    configuration.minimumScore === null ||
    configuration.minimumScore <= verdict().score
      ? 1
      : 0;
  assert.equal(result.contacts.length, expected);
  assert.equal(result.status, expected ? "succeeded" : "no_qualified_contacts");
});

await check(
  "three is a suggestion; top 3, 5, 10 or more and all work with every enrichment choice",
  async () => {
    // The repository default is a proposal to confirm, not a universal constant.
    if (infraPath === localInfra) assert.equal(configuration.topN, 3);
    const rows = Array.from({ length: 12 }, (_, i) => candidate(String(i + 1)));
    for (const fields of enrichmentPolicies)
      for (const topN of [1, 3, 5, 10, 25, null]) {
        const { result, calls } = await exercise({
          policy: { ...fields, topN },
          rows,
        });
        const expectedCount = Math.min(topN ?? rows.length, rows.length);
        assert.equal(result.contacts.length, expectedCount);
        assert.equal(
          calls.filter((c) => c.slug === "profile").length,
          rows.length,
        );
        assert.equal(
          calls.filter((c) => c.slug === "qualify").length,
          rows.length,
        );
        for (const [field, slug] of [
          ["email", "email_lookup"],
          ["phone", "phone_lookup"],
        ])
          assert.equal(
            calls.filter((c) => c.slug === slug).length,
            fields[field] ? expectedCount : 0,
          );
      }
  },
);

await check(
  "OpenAI and Claude qualification agents preserve schema, evidence and failures",
  async () => {
    assert.deepEqual(
      qualificationAgentSettings.output.jsonSchema,
      qualificationSchema,
    );
    assert.equal(qualificationAgentSettings.maxSteps, 1);
    assert.equal(qualificationAgentSettings.harness, undefined);
    for (const key of ["capabilities", "uses", "mcpClients", "triggers"])
      assert.deepEqual(qualificationAgentSettings[key], []);
    for (const policy of qualificationPolicies.slice(1)) {
      const { result, graph } = await exercise({ policy });
      assert.equal(result.contacts[0].qualification.score, verdict().score);
      assert.deepEqual(
        result.contacts[0].qualification.evidence,
        verdict().evidence,
      );
      assert.equal(
        walk(graph.nodes).filter((n) => n.kind === "agent").length,
        1,
      );
      assert.equal(
        walk(graph.nodes).some((n) => n.actionSlug === "instruct"),
        false,
      );
      const invalid = await exercise({ policy, answers: { 1: { score: 8 } } });
      assert.equal(invalid.result.status, "qualification_failed");
      const failed = await exercise({ policy, failure: ["qualify"] });
      assert.equal(failed.result.contacts.length, 0);
      assert.equal(failed.result.coverage.qualificationFailures, 1);
    }
  },
);

await check(
  "ID bypasses company lookup; no CRM, agent, model or schedule",
  async () => {
    const { result, calls, graph } = await exercise({
      input: {
        companyId: "00123",
        accountContext: { businessUnit: "capital projects" },
      },
    });
    assert.equal(result.status, "succeeded");
    assert.equal(result.account.companyId, "123");
    assert.equal(calls[0].slug, "search");
    assert.equal(
      walk(graph.nodes).filter(
        (n) =>
          n.actionSlug === "enrichCompany" ||
          n.actionSlug === "enrichCompanyFromDomain",
      ).length,
      0,
    );
    assert.equal(
      walk(graph.nodes).some(
        (n) => n.kind === "agent" || n.integrationSlug === "hubspot",
      ),
      false,
    );
  },
);
for (const [inputMode, input, slug] of [
  ["url", { linkedinCompanyUrl: company.linkedin_url }, "resolve_url"],
  [
    "domain",
    { domain: "https://www.infrastructure.example/path" },
    "resolve_domain",
  ],
]) {
  await check(`${inputMode} resolves before sourcing`, async () => {
    const { calls, result } = await exercise({ policy: { inputMode }, input });
    assert.equal(calls[0].slug, slug);
    assert.equal(calls[1].slug, "search");
    assert.equal(result.status, "succeeded");
  });
}
await check(
  "unresolved, ambiguous and conflicting input cannot search",
  async () => {
    for (const scenario of [
      { input: {} },
      { input: { companyId: "not-an-id" } },
      {
        policy: { inputMode: "multiple" },
        input: {
          companyId: "123",
          linkedinCompanyUrl: "https://linkedin.com/company/456",
        },
      },
      {
        policy: { inputMode: "multiple" },
        input: { companyId: "123", domain: "unverified.example" },
      },
      {
        policy: { inputMode: "domain" },
        input: { domain: "infrastructure.example" },
        failure: ["resolve_domain"],
      },
      {
        policy: { inputMode: "domain" },
        input: { domain: "infrastructure.example" },
        profiles: { company: { ...company, domain: "other.example" } },
      },
      {
        policy: { inputMode: "domain" },
        input: { domain: "infrastructure.example" },
        profiles: { company: { ...company, ambiguous: true } },
      },
      {
        policy: { inputMode: "url" },
        input: { linkedinCompanyUrl: company.linkedin_url },
        profiles: { company: {} },
      },
    ]) {
      const { result, calls } = await exercise(scenario);
      assert.equal(result.status, "company_not_resolved");
      assert.equal(
        calls.some((c) => c.slug === "search"),
        false,
      );
    }
  },
);
await check(
  "multiple input prefers ID with existing resolution, then URL, then domain",
  async () => {
    const policy = { inputMode: "multiple" };
    const { calls } = await exercise({
      policy,
      input: {
        companyId: "123",
        linkedinCompanyUrl: company.linkedin_url,
        domain: company.domain,
        resolvedCompany: company,
      },
    });
    assert.equal(calls[0].slug, "search");
    const url = await exercise({
      policy,
      input: {
        linkedinCompanyUrl: company.linkedin_url,
        domain: company.domain,
      },
    });
    assert.equal(url.calls[0].slug, "resolve_url");
    assert.equal(
      url.calls.some((c) => c.slug === "resolve_domain"),
      false,
    );
    const host = await exercise({ policy, input: { domain: company.domain } });
    assert.equal(host.calls[0].slug, "resolve_domain");
  },
);
await check(
  "deduplicate stable identity before profile and qualification spend",
  async () => {
    const rows = [
      candidate("1"),
      {
        ...candidate("1"),
        linkedin_profile_url: "https://linkedin.com/in/fictional-1/?source=x",
      },
      { ...candidate("1"), linkedin_profile_id: null },
      candidate("2"),
    ];
    const { result, calls } = await exercise({ rows });
    assert.equal(result.coverage.duplicates, 2);
    assert.equal(result.contacts.length, 2);
    assert.equal(calls.filter((c) => c.slug === "profile").length, 2);
    assert.equal(calls.filter((c) => c.slug === "qualify").length, 2);
    const conflict = await exercise({
      rows: [candidate("1"), { ...candidate("1"), linkedin_profile_id: 2 }],
    });
    assert.equal(conflict.result.coverage.identityConflicts, 2);
    assert.equal(conflict.calls.filter((c) => c.slug === "profile").length, 0);
  },
);
await check(
  "wrong employer and misleading titles are excluded; sparse evidence stays identifiable",
  async () => {
    const { result } = await exercise({
      rows: [
        candidate("1"),
        candidate("2", "Planning Manager"),
        candidate("3"),
      ],
      profiles: {
        1: profile("1", {
          experiences: [{ company_id: "999", is_current: true }],
        }),
        3: profile("3", { about: "", experiences: [] }),
      },
      answers: {
        1: verdict(10),
        2: verdict(1, {
          status: "not_relevant",
          explanation: "Financial planning, not project scheduling.",
        }),
        3: verdict(2, {
          status: "insufficient_evidence",
          employment: "uncertain",
          evidence: [],
        }),
      },
    });
    assert.equal(result.contacts.length, 0);
    assert.equal(result.coverage.notRelevant, 2);
    assert.equal(result.insufficientEvidence.length, 1);
    assert.equal(result.status, "no_qualified_contacts");
  },
);
await check(
  "practitioner outranks executive; numeric scores and stable identity ties",
  async () => {
    const { result } = await exercise({
      rows: [
        candidate("3", "Executive"),
        candidate("2"),
        candidate("1"),
        candidate("4"),
      ],
      answers: { 3: verdict(2), 2: verdict(10), 1: verdict(10), 4: verdict(8) },
    });
    assert.deepEqual(
      result.contacts.map((c) => c.identity),
      ["id:1", "id:2", "id:4", "id:3"],
    );
    assert.deepEqual(
      result.contacts.map((c) => c.rank),
      [1, 2, 3, 4],
    );
  },
);
await check("invalid AI output cannot enter the ranking", async () => {
  for (const answer of [
    verdict("9"),
    verdict(11),
    verdict(NaN),
    { score: 8 },
    null,
  ]) {
    const { result } = await exercise({ answers: { 1: answer } });
    assert.equal(result.status, "qualification_failed");
    assert.equal(result.contacts.length, 0);
    assert.equal(result.coverage.qualificationFailures, 1);
  }
  for (const answer of [
    verdict(9, { evidence: [] }),
    verdict(9, { matchedPersona: "invented_persona" }),
    verdict(9, { employment: "uncertain" }),
  ]) {
    const { result } = await exercise({ answers: { 1: answer } });
    assert.equal(result.contacts.length, 0);
    assert.equal(result.insufficientEvidence.length, 1);
  }
});
await check(
  "profile identity mismatch and concurrent advisory role do not qualify",
  async () => {
    const mismatch = await exercise({ profiles: { 1: profile("2") } });
    assert.equal(mismatch.result.contacts.length, 0);
    const side = await exercise({
      profiles: {
        1: profile("1", {
          experiences: [
            { company_id: "123", is_current: true, title: "Community advisor" },
            { company_id: "999", is_current: true, title: "Primary employer" },
          ],
        }),
      },
      answers: {
        1: verdict(0, { status: "not_relevant", employment: "wrong_employer" }),
      },
    });
    assert.equal(side.result.contacts.length, 0);
  },
);
await check(
  "search failures differ from zero matches and qualification failures",
  async () => {
    const empty = await exercise({ rows: [] });
    assert.equal(empty.result.status, "no_qualified_contacts");
    const search = await exercise({ failure: ["search"] });
    assert.equal(search.result.status, "search_failed");
    assert.equal(search.result.coverage.searchFailures, 1);
    const qualification = await exercise({ failure: ["qualify"] });
    assert.equal(qualification.result.status, "qualification_failed");
    const retrieval = await exercise({ failure: ["profile"] });
    assert.equal(retrieval.result.coverage.profileFailures, 1);
    assert.equal(
      retrieval.calls.some((c) => c.slug === "qualify"),
      false,
    );
    const partial = await exercise({
      rows: [candidate("1"), candidate("2")],
      failure: ["qualify:id:1"],
    });
    assert.equal(partial.result.status, "partial");
    assert.equal(partial.result.contacts.length, 1);
  },
);
await check(
  "search cap discloses provider page rounding and bounds profile spend",
  async () => {
    const { result, calls } = await exercise({
      policy: { searchLimit: 30 },
      rows: Array.from({ length: 50 }, (_, i) => candidate(String(i + 1))),
    });
    assert.equal(calls[0].data.limit, 50);
    assert.equal(result.coverage.returned, 50);
    assert.equal(result.coverage.examined, 30);
    assert.equal(result.coverage.searchCapReached, true);
    assert.equal(result.contacts.length, 30);
  },
);
await check(
  "without enrichment there are no email, verification or phone nodes",
  async () => {
    const { graph, calls } = await exercise();
    assert.equal(
      walk(graph.nodes).some(
        (n) => n.kind === "tool" || n.actionSlug === "verifyEmail",
      ),
      false,
    );
    assert.equal(calls.length, 3);
  },
);
await check(
  "all or up to N is independent of enrichment and limits only sorted qualified people",
  async () => {
    for (const fields of enrichmentPolicies) {
      for (const topN of [null, 2, 7]) {
        const { result, calls } = await exercise({
          policy: { ...fields, topN },
          rows: ["1", "2", "3", "4", "5"].map((id) => candidate(id)),
          answers: {
            1: verdict(10, { status: "not_relevant" }),
            2: verdict(7),
            3: verdict(9),
            4: verdict(10, { status: "insufficient_evidence" }),
            5: verdict(8),
          },
        });
        const expected =
          topN === 2 ? ["id:3", "id:5"] : ["id:3", "id:5", "id:2"];
        assert.deepEqual(
          result.contacts.map((c) => c.identity),
          expected,
        );
        assert.deepEqual(
          result.contacts.map((c) => c.rank),
          expected.map((_, i) => i + 1),
        );
        assert.equal(result.coverage.qualified, 3);
        assert.equal(result.coverage.selected, expected.length);
        assert.equal(result.insufficientEvidence.length, 1);
        assert.equal(calls.filter((c) => c.slug === "profile").length, 5);
        assert.equal(calls.filter((c) => c.slug === "qualify").length, 5);
        for (const [field, slug] of [
          ["email", "email_lookup"],
          ["phone", "phone_lookup"],
        ]) {
          assert.deepEqual(
            calls.filter((c) => c.slug === slug).map((c) => c.identity),
            fields[field] ? expected : [],
          );
        }
      }
      const empty = await exercise({
        policy: { ...fields, topN: 2 },
        rows: [],
      });
      assert.deepEqual(empty.result.contacts, []);
      assert.equal(empty.result.status, "no_qualified_contacts");
    }
  },
);
await check(
  "shortlist selects N first, keeps original profiles and rank after reversed enrichment",
  async () => {
    const { result, calls } = await exercise({
      policy: {
        ...emailPolicy,
        phone: true,
        phoneToolUuid: phonePolicy.phoneToolUuid,
        topN: 2,
      },
      rows: [candidate("1"), candidate("2"), candidate("3")],
      answers: { 1: verdict(7), 2: verdict(9), 3: verdict(8) },
    });
    assert.deepEqual(
      result.contacts.map((c) => c.identity),
      ["id:2", "id:3"],
    );
    assert.deepEqual(
      result.contacts.map((c) => c.rank),
      [1, 2],
    );
    assert.equal(calls.filter((c) => c.slug === "profile").length, 3);
    assert.equal(calls.filter((c) => c.slug === "email_lookup").length, 2);
    assert.equal(calls.filter((c) => c.slug === "phone_lookup").length, 2);
    assert.deepEqual(result.contacts[0].profile, profile("2"));
    assert.deepEqual(
      result.contacts[0].qualification.evidence,
      verdict().evidence,
    );
  },
);
await check(
  "email-only cannot call phone; phone-only cannot call email",
  async () => {
    const email = await exercise({ policy: emailPolicy });
    assert.equal(
      email.calls.some((c) => c.slug === "phone_lookup"),
      false,
    );
    assert.equal(email.result.contacts[0].verificationStatus, "verified");
    const phone = await exercise({ policy: phonePolicy });
    assert.equal(
      phone.calls.some((c) =>
        ["email_lookup", "verify_email"].includes(c.slug),
      ),
      false,
    );
    assert.equal(phone.result.contacts[0].emailStatus, "not_requested");
  },
);
await check(
  "selected contact failures are retained with no backfill",
  async () => {
    const { result, calls } = await exercise({
      policy: { ...emailPolicy, topN: 1 },
      rows: [candidate("1"), candidate("2")],
      failure: ["email_lookup:id:1"],
    });
    assert.equal(result.contacts.length, 1);
    assert.equal(result.contacts[0].identity, "id:1");
    assert.equal(result.contacts[0].emailStatus, "failed");
    assert.equal(result.contacts[0].rank, 1);
    assert.equal(result.status, "partial");
    assert.equal(calls.filter((c) => c.slug === "email_lookup").length, 1);
  },
);
await check(
  "found email is not verified; verification failure stays explicit",
  async () => {
    for (const options of [
      { failure: ["verify_email"] },
      { verification: { "id:1": { email_status: "catch_all" } } },
      { verification: { "id:1": { email_status: "invalid" } } },
    ]) {
      const { result } = await exercise({ policy: emailPolicy, ...options });
      assert.notEqual(result.contacts[0].verificationStatus, "verified");
      assert.equal(result.status, "partial");
      assert.ok(result.contacts[0].email);
    }
  },
);
await check(
  "reuse suitable existing contact data; ignore stale or conflicting values",
  async () => {
    const input = {
      companyId: "123",
      knownContacts: [
        {
          personId: "1",
          email: "approved@infrastructure.example",
          verificationStatus: "verified",
          emailMeetsRequirements: true,
          phone: "+12025550123",
          phoneMeetsRequirements: true,
        },
      ],
    };
    const policy = {
      ...emailPolicy,
      phone: true,
      phoneToolUuid: phonePolicy.phoneToolUuid,
    };
    const { result, calls } = await exercise({ policy, input });
    assert.equal(result.contacts[0].emailStatus, "reused");
    assert.equal(result.contacts[0].phoneStatus, "reused");
    assert.equal(
      calls.some((c) =>
        ["email_lookup", "verify_email", "phone_lookup"].includes(c.slug),
      ),
      false,
    );
    const stale = await exercise({
      policy: emailPolicy,
      input: {
        ...input,
        knownContacts: [
          { ...input.knownContacts[0], emailMeetsRequirements: false },
        ],
      },
    });
    assert.ok(stale.calls.some((c) => c.slug === "email_lookup"));
  },
);
await check(
  "fewer than N and operator-selected threshold have deterministic output",
  async () => {
    const fewer = await exercise({ policy: { ...emailPolicy, topN: 7 } });
    assert.equal(fewer.result.contacts.length, 1);
    const threshold = await exercise({ policy: { minimumScore: 9 } });
    assert.equal(threshold.result.contacts.length, 0);
    assert.equal(threshold.result.coverage.belowThreshold, 1);
  },
);
await check(
  "all installation variants compile and omit unused routes",
  async () => {
    for (const inputMode of ["id", "url", "domain", "multiple"]) {
      for (const topN of [null, 2]) {
        for (const mode of enrichmentPolicies) {
          for (const qualification of qualificationPolicies) {
            const graph = buildContactSourcing(
              {
                ...configuration,
                inputMode,
                ...mode,
                topN,
                ...qualification,
              },
              agentFixtureUuid,
            );
            validateGraph(graph.nodes);
            const planned = await compile({
              nodes: resources().map((resource) =>
                resource.id === "tool:contact_sourcing"
                  ? {
                      ...resource,
                      spec: {
                        ...resource.spec,
                        nodes: graph.nodes,
                        formFields: graph.formFields,
                      },
                    }
                  : resource,
              ),
            });
            assert.deepEqual(
              planned.errors,
              [],
              "every variant must pass the actual CDK compiler/planner",
            );

            assert.equal(
              walk(graph.nodes).some((n) => n.slug === "phone_lookup"),
              !!mode.phone,
            );
            assert.equal(
              walk(graph.nodes).some((n) => n.slug === "email_lookup"),
              !!mode.email,
            );
            const selected = graph.nodes.find((n) => n.slug === "selected");
            assert.equal(!!selected, topN !== null || mode.email || mode.phone);
            if (selected)
              assert.equal(
                selected.config.variables[0].value.expression,
                topN === null
                  ? "{{nodes.rank.result.contacts}}"
                  : "{{nodes.rank.result.contacts.slice(0, 2)}}",
              );
          }
        }
      }
    }
    assert.throws(() =>
      buildContactSourcing({ ...configuration, searchLimit: 0 }),
    );
    assert.throws(() =>
      buildContactSourcing({
        ...configuration,
        email: true,
        emailToolUuid: undefined,
      }),
    );
    for (const topN of [0, -1, 1.5, NaN, Infinity])
      for (const fields of enrichmentPolicies)
        assert.throws(
          () => buildContactSourcing({ ...configuration, ...fields, topN }),
          /topN/,
        );
  },
);

await check(
  "accepted feedback updates reusable search, qualification and output version",
  async () => {
    const criteria =
      configuration.sellerCriteria +
      " Exclude financial forecasting; include schedule assurance.";
    const { result, calls } = await exercise({
      policy: {
        criteriaVersion: "operator-feedback-v2",
        sellerCriteria: criteria,
        titleKeywords: ["schedule assurance"],
        titleKeywordsExclude: ["financial forecasting"],
      },
    });
    assert.equal(result.criteriaVersion, "operator-feedback-v2");
    assert.deepEqual(
      calls.find((c) => c.slug === "search").data.role.titleKeywords,
      ["schedule assurance"],
    );
    assert.deepEqual(
      calls.find((c) => c.slug === "search").data.role.titleKeywordsExclude,
      ["financial forecasting"],
    );
    assert.ok(
      calls.find((c) => c.slug === "qualify").data.prompt.includes(criteria),
    );
  },
);
await check(
  "invalid ID can fall through to a valid URL with a warning",
  async () => {
    const { result, calls } = await exercise({
      policy: { inputMode: "multiple" },
      input: {
        companyId: "a-crm-id",
        linkedinCompanyUrl: company.linkedin_url,
      },
    });
    assert.equal(calls[0].slug, "resolve_url");
    assert.equal(result.status, "succeeded");
    assert.deepEqual(result.warnings, ["invalid_company_id_ignored"]);
  },
);

await check(
  "verification must match the found address and reuse must match person identity",
  async () => {
    const wrong = await exercise({
      policy: emailPolicy,
      verification: {
        "id:1": {
          email: "someone-else@infrastructure.example",
          email_status: "valid",
        },
      },
    });
    assert.equal(wrong.result.contacts[0].verificationStatus, "unknown");
    const conflict = await exercise({
      policy: emailPolicy,
      input: {
        companyId: "123",
        knownContacts: [
          {
            personId: "2",
            linkedinUrl: candidate("1").linkedin_profile_url,
            email: "wrong@infrastructure.example",
            verificationStatus: "verified",
            emailMeetsRequirements: true,
          },
        ],
      },
    });
    assert.ok(conflict.calls.some((c) => c.slug === "email_lookup"));
    assert.notEqual(
      conflict.result.contacts[0].email,
      "wrong@infrastructure.example",
    );
  },
);

// These assert presence of the installer gates, not the quality of an AI-led
// teaching session. acceptance.md covers the fresh-workspace blind test.
const read = (path) =>
  readFileSync(new URL(path, import.meta.url), "utf8").replace(/\s+/g, " ");
await check(
  "installer decisions, optional CRM research and reusable feedback are explicit",
  async () => {
    const audit = read("../references/audit.md");
    const configure = read("../references/configure.md");
    const run = read("../references/run.md");
    for (const fragment of [
      "website research alone",
      "operator chooses",
      "source URLs",
      "Observed",
      "inference",
      "Are these the right people to target?",
      "Can you confirm this job-title Boolean",
      "context graph",
    ])
      assert.ok(audit.includes(fragment), fragment);
    for (const fragment of [
      "What company identifier",
      "How many qualified people should the tool return per company",
      "Independently, do you need verified work email",
      "already provides useful evidence",
      "recommend N",
      "Otherwise, ask directly",
      "Do not add a separate audit",
      "Do you have an OpenAI or Anthropic",
      "never paste",
      "slightly broader",
      "up to three",
      "Recommend",
      "tradeoff",
      "search limit",
    ])
      assert.ok(configure.includes(fragment), fragment);
    for (const fragment of [
      "maximum cost",
      "Are these the most relevant stakeholders",
      "reusable criteria",
      "Do you want to keep this as an on-demand tool",
      "Sample approval does not authorize a full batch",
    ])
      assert.ok(run.includes(fragment), fragment);
    assert.doesNotMatch(run, /would you approach them in this order/i);
  },
);
console.log(
  `Passed ${checks} contact-sourcing contracts (mocked external calls; no live provider runs).`,
);
