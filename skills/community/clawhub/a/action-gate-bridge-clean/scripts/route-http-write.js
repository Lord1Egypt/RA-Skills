#!/usr/bin/env node
const base = process.env.CRABTRAP_HTTP_PROXY_URL || "http://localhost:8795";

const [
  ,
  ,
  source = "communications",
  target = "http-target",
  summary = "HTTP write routed via action gate",
  path = "/",
  bodyJson = "{}",
  program = "External API",
  credentialsRef = "",
] = process.argv;

async function main() {
  const body = JSON.parse(bodyJson);
  const res = await fetch(`${base}/v1/http/requests`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      source,
      target,
      summary,
      program,
      execution: {
        adapter: "http_json",
        ...(credentialsRef ? { credentialsRef } : {}),
      },
      request: {
        method: "POST",
        path,
        body,
      },
    }),
  });
  console.log(JSON.stringify(await res.json(), null, 2));
}

main().catch((err) => {
  console.error(err.stack || String(err));
  process.exit(1);
});
