# Threat Model

What this skill is for, what it stops, and what it cannot stop. Read this before
relying on it.

## What is being protected

A workstation or server where OpenClaw runs as an ordinary user. The concern is
the agent, or content it reads, causing a privileged (root) command to run, or a
service to be exposed, without the owner deciding that it should.

## Who the controls are aimed at

| Actor | Example |
| --- | --- |
| An agent acting on a mistaken or injected instruction | A web page or message tells the agent to run `sudo ...` |
| An agent acting carelessly | It reaches for `sudo` to get past a permission error |
| Configuration drift | A new listening port, an outbound connection to a new host, an old OpenClaw release |

## What holds, and why

| Control | Holds against an agent running as your user? | Why |
| --- | --- | --- |
| sudo's password prompt | Yes | Enforced by the operating system. The agent does not know the password. The guard discards cached sudo credentials so the prompt appears every time. |
| Approval prompt on the terminal | Yes, when the agent has no terminal | The prompt is read from the controlling terminal, not stdin, so piping an answer does nothing. With no terminal the command is refused. |
| Command policy (deny rules) | Partly | It blocks listed commands that go through the guard. It is a pattern match on the command line, so it is a safety net, not a sandbox. |
| Signed session state | Partly | Stops accidental and casual edits. The signing key is in your account, so a determined process running as you could forge a state file. |
| Hash-chained audit log | Partly | Detects edited, removed or inserted entries. A process running as you could replace the whole file with a new chain. |
| sudo shim on the gateway's PATH | No, on its own | It routes ordinary `sudo` calls through the guard. Calling `/usr/bin/sudo` by its full path goes around it, and then meets sudo's password prompt. |
| Port, egress and compliance checks | Detective only | They report every 30 minutes. They do not block anything. |

## What this does not protect against

- **Anything the agent can do as your user without root.** Reading your files,
  deleting your documents, sending data out, changing its own configuration.
  Use OpenClaw's own sandbox and tool permissions for that.
- **Passwordless sudo.** If sudoers has a `NOPASSWD` rule for your user, sudo's
  prompt, the one control that fully holds, is gone. The
  `alternate_privilege_paths_restricted` control reports this as a violation.
- **An agent that has been given a terminal.** A process that owns a pseudo-terminal
  can type into the approval prompt. It still cannot answer sudo's password prompt.
- **Tampering with this skill's own files.** The scripts, policies and reports live
  in your account. A process running as you can change them. Ship the audit log to
  another system if you need evidence that survives that.
- **Events between scans.** A port opened and closed, or a connection made and
  dropped, between two 30-minute cycles is not seen.
- **UDP and non-TCP traffic** in the egress monitor, and UDP listeners unless
  `--include-udp` is used.
- **Other escalation tools** such as `su` or `doas`, beyond reporting on sudo.

## Recommendations

1. Keep a password on sudo. Do not add `NOPASSWD` for the user OpenClaw runs as.
2. Install the sudo shim and reload the gateway so ordinary `sudo` calls are logged
   and policy-checked.
3. Write deny rules for commands you never want run as root.
4. Review the dashboard, and treat `summary.evaluated: 0` in an egress report as
   "nothing was checked".
5. If you need the audit trail as evidence, copy `privileged-audit.jsonl` to a
   system the agent cannot write to.
