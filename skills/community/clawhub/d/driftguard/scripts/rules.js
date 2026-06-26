const NODE_PROCESS_MODULE = ["child", "process"].join("_");

const SHELL_PATTERNS = [
  {
    id: "shell.curl_pipe",
    severity: "critical",
    description: "Pipe curl output into shell",
    rationale: "Downloads remote content and executes it immediately, which can run attacker-controlled code without review.",
    review: "Verify the URL owner, pin expected content or checksum, and replace pipe-to-shell with an explicit reviewed script when possible.",
    regex: /curl\s+[^\n]*\|\s*(sh|bash)\b/i
  },
  {
    id: "shell.wget_pipe",
    severity: "critical",
    description: "Pipe wget output into shell",
    rationale: "Downloads remote content and executes it immediately, which can run attacker-controlled code without review.",
    review: "Verify the URL owner, pin expected content or checksum, and replace pipe-to-shell with an explicit reviewed script when possible.",
    regex: /wget\s+[^\n]*\|\s*(sh|bash)\b/i
  },
  {
    id: "shell.eval",
    severity: "high",
    description: "Dynamic eval execution",
    rationale: "Dynamically executes strings as code, so untrusted input can become arbitrary code execution.",
    review: "Confirm the evaluated string is fully controlled and cannot include user, network, or file input.",
    regex: /\beval\s*\(/i
  },
  {
    id: "shell.exec_node",
    severity: "high",
    description: "Node process execution",
    rationale: "Can spawn OS commands from JavaScript, which may modify files, exfiltrate data, or run downloaded payloads.",
    review: "Check command construction, input escaping, allowlists, and whether shell execution is truly required.",
    regex: new RegExp(`${NODE_PROCESS_MODULE}\\s*\\.\\s*(exec|execSync|spawn|spawnSync)\\s*\\(`, "i")
  },
  {
    id: "shell.exec_generic",
    severity: "low",
    confidence: "low",
    scored: false,
    description: "Generic exec call (low confidence)",
    rationale: "The term exec can indicate command execution, but it is noisy across languages and APIs, so it is shown for context only.",
    review: "Confirm whether this is actually OS command execution. If benign, suppress the rule for this path.",
    regex: /\bexec\s*\(/i
  },
  {
    id: "shell.os_system",
    severity: "high",
    description: "os.system call",
    rationale: "Executes a shell command from Python, which can become command injection if any input is variable.",
    review: "Prefer subprocess with argument arrays, avoid shell interpolation, and validate all inputs.",
    regex: /\bos\.system\s*\(/i
  },
  {
    id: "shell.subprocess",
    severity: "high",
    description: "Python subprocess usage",
    rationale: "Runs external processes from Python. This is powerful and risky when commands or arguments are user-controlled.",
    review: "Check whether arguments are fixed, safely escaped, and necessary. Watch for network downloads or sensitive file reads nearby.",
    regex: /\bsubprocess\.(Popen|call|run|check_output)\s*\(/i
  },
  {
    id: "shell.shell_true",
    severity: "high",
    description: "Python subprocess shell=True",
    rationale: "Runs through a shell, increasing command injection risk when any part of the command is variable.",
    review: "Remove shell=True when possible and pass command arguments as an array.",
    regex: /shell\s*=\s*True/
  },
  {
    id: "shell.runtime_exec",
    severity: "high",
    description: "Java Runtime exec",
    rationale: "Runs OS commands from Java and can execute arbitrary system-level behavior.",
    review: "Check command construction, input validation, and whether a safer library call can replace it.",
    regex: /Runtime\.getRuntime\s*\(\)\.exec\s*\(/i
  },
  {
    id: "shell.process_builder",
    severity: "medium",
    description: "Java ProcessBuilder usage",
    rationale: "Starts external processes. It can be legitimate, but it expands the tool's capabilities beyond normal code execution.",
    review: "Confirm commands are static or allowlisted and do not process untrusted input.",
    regex: /new\s+ProcessBuilder\s*\(/i
  },
  {
    id: "shell.sh_c",
    severity: "medium",
    description: "Shell command with -c",
    rationale: "Runs a command string through a shell, which can hide chained commands or injection risk.",
    review: "Inspect the full command string and prefer direct argument execution where possible.",
    regex: /\b(sh|bash)\s+-c\b/i
  }
];

const NETWORK_PATTERNS = [
  {
    id: "net.fetch",
    severity: "medium",
    description: "JavaScript fetch call",
    rationale: "Adds outbound network access. This can be legitimate, but it may send data out or fetch remote instructions/payloads.",
    review: "Check destination URLs, transmitted data, authentication handling, and whether calls are user-triggered or automatic.",
    regex: /\bfetch\s*\(/i
  },
  {
    id: "net.axios",
    severity: "medium",
    description: "Axios HTTP client usage",
    rationale: "Adds outbound HTTP capability, which can exfiltrate local data or retrieve remote content.",
    review: "Confirm allowed hosts, request bodies, headers, and error logging do not expose secrets.",
    regex: /\baxios\s*\./i
  },
  {
    id: "net.requests",
    severity: "medium",
    description: "Python requests usage",
    rationale: "Adds outbound HTTP capability, which can exfiltrate local data or retrieve remote content.",
    review: "Confirm allowed hosts, request bodies, headers, and error logging do not expose secrets.",
    regex: /\brequests\.(get|post|put|delete|patch)\s*\(/i
  },
  {
    id: "net.curl",
    severity: "medium",
    description: "curl invocation",
    rationale: "Uses a command-line network client. Risk increases if combined with shell execution or sensitive file access.",
    review: "Check URL, flags, uploaded data, redirects, and whether output is executed or written to trusted paths.",
    regex: /\bcurl\s+https?:\/\//i
  },
  {
    id: "net.wget",
    severity: "medium",
    description: "wget invocation",
    rationale: "Uses a command-line network client. Risk increases if downloaded content is executed or trusted automatically.",
    review: "Check URL, flags, destination path, and whether output is executed or used as configuration.",
    regex: /\bwget\s+https?:\/\//i
  },
  {
    id: "net.webhook",
    severity: "medium",
    description: "Webhook mention",
    rationale: "Webhook integrations commonly send data to external systems and may expose event payloads or secrets.",
    review: "Confirm what payload is sent, where it goes, and whether secrets are redacted.",
    regex: /\bwebhook\b/i
  },
  {
    id: "net.http_module",
    severity: "medium",
    description: "Node http/https request",
    rationale: "Adds low-level outbound HTTP capability, which can transmit data or fetch remote content.",
    review: "Check host allowlists, request payloads, TLS handling, and whether responses affect execution.",
    regex: /\bhttps?\.request\s*\(/i
  }
];

const SENSITIVE_PATH_PATTERNS = [
  {
    id: "sensitive.env",
    severity: "high",
    description: "Reference to .env file",
    rationale: ".env files often contain API keys, tokens, database URLs, or private configuration. Risk is high because exposure can compromise accounts.",
    review: "Confirm the code does not read, print, upload, commit, or copy secrets from .env files.",
    regex: /(^|[\\/"'`\s])\.env(?:\.[A-Za-z0-9_-]+)?\b/i
  },
  {
    id: "sensitive.ssh_key",
    severity: "critical",
    description: "Reference to SSH key",
    rationale: "SSH private keys can grant direct machine or repository access. Exposure is a severe credential compromise.",
    review: "Confirm private keys are never read, logged, copied, uploaded, or bundled. Rotate any exposed key.",
    regex: /(id_rsa|id_ed25519|\.ssh\b)/i
  },
  {
    id: "sensitive.openclaw",
    severity: "low",
    description: "OpenClaw config reference",
    rationale: "OpenClaw config references may be benign, but config can reveal local setup or tool capabilities.",
    review: "Check whether the file is only documented or whether config values are read, modified, or transmitted.",
    regex: /openclaw\.(json|toml|yaml|yml)/i
  },
  {
    id: "sensitive.driftguard",
    severity: "low",
    scored: false,
    confidence: "low",
    description: "Driftguard config reference",
    rationale: "Scanner config references are usually expected, but can affect which paths or rules are ignored.",
    review: "Confirm suppressions are narrow and do not hide meaningful risk.",
    regex: /\.driftguard\.json\b/i
  },
  {
    id: "sensitive.soul",
    severity: "low",
    description: "Reference to SOUL.md",
    rationale: "SOUL.md can contain persona or private context. References are low risk unless the file is read or shared.",
    review: "Confirm the content is not copied into prompts, logs, reports, or network requests without intent.",
    regex: /SOUL\.md/i
  },
  {
    id: "sensitive.memory",
    severity: "low",
    description: "Reference to MEMORY.md",
    rationale: "MEMORY.md can contain private long-term user context. References are low risk unless the file is read or shared.",
    review: "Confirm the content is not copied into prompts, logs, reports, or network requests without intent.",
    regex: /MEMORY\.md/i
  }
];

const PROMPT_INJECTION_PATTERNS = [
  {
    id: "prompt.ignore_previous",
    severity: "high",
    description: "Prompt injection: prior-instruction override",
    rationale: "Attempts to override prior instructions can hijack agent behavior when loaded into an LLM context.",
    review: "Treat as untrusted content. Confirm it is documentation/test data, not operational instructions for the agent.",
    regex: /(ignore|disregard|forget)\s+(all\s+)?(previous|prior)\s+instructions/i
  },
  {
    id: "prompt.override_system",
    severity: "high",
    description: "Prompt injection: override system/developer",
    rationale: "Attempts to bypass system or safety instructions can redirect an agent away from trusted rules.",
    review: "Confirm the text is inert sample data or remove it from loaded prompt surfaces.",
    regex: /(override|bypass|jailbreak)\s+(system|developer|safety)/i
  },
  {
    id: "prompt.roleplay",
    severity: "medium",
    description: "Prompt injection: roleplay/system prompt mention",
    rationale: "Roleplay or system-prompt language can be benign, but may influence an agent if included in loaded instructions.",
    review: "Check whether the file is loaded as instructions. If yes, isolate or quote it as untrusted content.",
    regex: /(system prompt|developer message|you are chatgpt|act as)/i
  },
  {
    id: "prompt.tools",
    severity: "medium",
    description: "Prompt injection: tool execution coercion",
    rationale: "Text that tells an agent to execute commands can become dangerous if treated as instructions.",
    review: "Confirm the command text is sample data, documentation, or explicitly fenced as untrusted.",
    regex: /(execute|run)\s+(this|the)\s+(command|script|tool)/i
  }
];

const OBFUSCATION_PATTERNS = [
  {
    id: "obfuscation.base64",
    severity: "medium",
    description: "Base64 encode/decode usage",
    rationale: "Encoding/decoding can be legitimate, but it can also hide payloads, commands, or exfiltrated data.",
    review: "Inspect decoded content and check whether it is executed, written to disk, or sent over the network.",
    regex: /\b(base64|b64decode|atob|btoa)\b/i
  },
  {
    id: "obfuscation.long_base64",
    severity: "medium",
    description: "Suspicious long base64-like string",
    rationale: "Long encoded blobs can hide code, secrets, or payloads from review.",
    review: "Decode in a safe local environment and confirm the content is expected and non-executable.",
    regex: /[A-Za-z0-9+\/]{200,}={0,2}/
  },
  {
    id: "obfuscation.long_hex",
    severity: "medium",
    description: "Suspicious long hex string",
    rationale: "Long hex blobs can hide payloads or embedded binary data from review.",
    review: "Decode or identify the blob and confirm it is expected, documented, and not executed.",
    regex: /\b[0-9a-fA-F]{80,}\b/
  }
];

module.exports = {
  SHELL_PATTERNS,
  NETWORK_PATTERNS,
  SENSITIVE_PATH_PATTERNS,
  PROMPT_INJECTION_PATTERNS,
  OBFUSCATION_PATTERNS
};
