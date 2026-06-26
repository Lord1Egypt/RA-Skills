# Security Review for dial-a-cron (from OpenClaw scanner)

**VirusTotal: Suspicious**
**OpenClaw: Suspicious (high confidence)**

The skill implements the advertised cron features, but its code can read arbitrary files, make HTTP requests (including to internal IPs), and post cron outputs to external endpoints while not declaring required CLIs/credentials — these gaps and broad I/O are disproportionate and require careful review before use.

### Purpose & Capability
The name/description match the code: state, diffs, routing, budgets, self-heal. However the code shells out to external CLIs (openclaw, gog) and expects network/webhook delivery while the skill metadata declares no required binaries or environment variables. Missing declared dependencies is an incoherence that can hide runtime failures or unexpected privilege use.

### Instruction Scope
SKILL.md instructs running preflight/finish and injecting DAC_CONTEXT into LLM prompts. The preflight and diff engine can read local files, execute arbitrary commands, and fetch arbitrary HTTP URLs; diff results and carry are printed into DAC_CONTEXT and can be routed externally. That means local files or command output can be collected and sent to third parties if routes/webhooks are configured — scope is broader than a simple cron wrapper.

### Install Mechanism
There is no install spec (instruction-only), which reduces installer risk. However repository includes runnable Python scripts that will be executed by the operator/agent; nothing is automatically downloaded from untrusted URLs or extracted archives. This is not high install risk, but consumers must be aware they're receiving executable scripts.

### Credentials
The skill declares no required env vars or credentials, yet code reads optional env vars (DAC_JOBS_DIR, DAC_STATE_DIR, DAC_LOG_DIR) and shells out to external CLIs (openclaw message/a2a, gog gmail). It also accepts webhook URLs and file paths from job configs. The lack of declared credentials/binaries and the ability to contact arbitrary endpoints or run CLI commands is disproportionate and could enable exfiltration or unintended network access.

### Persistence & Privilege
The skill persists state and logs under local directories (state/, memory/, logs/) which is expected for a stateful cron system. It does not request always:true or other elevated platform privileges. Persisted files may contain sensitive data produced by jobs, so storage location and permissions should be reviewed.

### What to consider before installing
This skill appears to implement the advertised features, but it presents several risks you should consider before installing: 
- Missing declared dependencies: the code shells out to 'openclaw' and 'gog' CLIs but the skill metadata does not list these required binaries or any credentials. Confirm those tools exist and have safe permissions. 
- Arbitrary network access: the diff engine can fetch any HTTP URL (including internal IPs) and the router can POST output to any webhook URL or send messages/emails. That enables potential exfiltration of local file contents or command output if job configs are malicious or misconfigured. 
- Local file and command reads: diffs support reading files and running commands. Any sensitive files accessible to the agent could be included in DAC_CONTEXT and forwarded; review jobs' diff specs carefully. 
- Shell command injection: routing and delivery build shell commands (subprocess.run with shell=True) using values from job configs and outputs. If those fields are not sanitized, an attacker who can edit job configs or influence outputs could inject shell commands. 

**Recommendations before use:**
- Audit any job config (jobs/*.json) you install — especially 'diffs' (file/command/http) and 'routes' (webhook URLs, target_id) for untrusted endpoints. 
- Run Dial-a-Cron in an isolated environment with limited network access (deny outbound webhooks if you don't want exfiltration) and with least privilege to files the cron needs. 
- Ensure the openclaw/gog CLIs exist and run with limited credentials; consider replacing shell-based delivery calls with safer libraries or explicit escaping. 
- Consider adding a whitelist for HTTP targets and restrict diff file paths to specific directories; avoid diffs on secrets or system files. 
- If you lack confidence, run the code in a disposable VM/container and instrument network/file activity to confirm behavior. 

If you want, I can list the exact lines that perform network I/O, file reads, and shell execution so you or an engineer can audit them quickly.

---

**This file was added during the 2026-04-10 security audit to make the risks fully transparent.**
