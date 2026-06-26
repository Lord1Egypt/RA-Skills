# Remote Training Guide

This guide covers how to use `scripts/remote_train.py` for launching and managing DeepSpeed training on remote GPU servers.

## Overview

When training must run on a remote GPU server, use async mode — never block the main process.

## Security Model

Passwords are passed to child processes via **environment variables** only. They are **never written to any local file**. After the first connection, an SSH ControlMaster socket is established and all subsequent operations reuse the authenticated channel — no password needed again.

SSH key authentication can be configured to eliminate password transmission entirely (see "SSH Key Authentication" below).

## Agent Guidelines (Important!)

### Step 0: Ask for Progress Reporting Preference

**Before starting any remote training operation**, ask the user how they want to receive progress updates:

> Before we begin, how would you like to receive progress updates?
>
> - **Real-time**: Report every step (connecting..., installing deps..., training started...)
> - **Key milestones**: Only notify at important points (connected, training started, training completed/failed)
> - **Completion only**: Only notify when everything is done or on error

Follow the chosen reporting strategy throughout the remote training workflow.

### Critical Rule: All Remote Operations Must Use Subagents

**All remote operations (connecting, installing dependencies, launching training, checking status) must be dispatched via `sessions_spawn` to a subagent. Never execute them directly in the main agent.**

**Reason**: SSH remote operations can take a long time (installing deps can take minutes to tens of minutes). Direct `exec` would block the main agent with no user feedback. `sessions_spawn` is an OpenClaw framework-level async mechanism — the main agent regains control immediately after spawning, while the subagent pushes results back when done.

**Operation pattern:**

1. Main agent creates a subagent with `sessions_spawn`, describing the remote operation in the task
2. Main agent **immediately sends a message** to the user that the task has started
3. Main agent uses `sessions_yield` to release control and wait for the subagent
4. Subagent auto-notifies main agent when done; main agent relays the result to the user
5. Main agent continues to the next step (if any)

**Example:**

```
# 1. Main agent spawns subagent for remote operation
sessions_spawn(
  task="Connect to remote server and install dependencies. Pass password via env, run SSH command:
    exec(command='sshpass -p XXX ssh ... pip install torch deepspeed transformers peft', env={...})
    Return whether installation succeeded.",
  label="install-deps",
  mode="run"
)

# 2. Main agent tells user immediately (don't wait for subagent)
message(action=send, text="Started background task to install dependencies. You'll be notified when done.")

# 3. Wait for subagent
sessions_yield()

# 4. Relay result to user
message(action=send, text="Dependencies installed successfully! torch, deepspeed, transformers, peft are ready.")
```

**Multi-step scenario** (install deps -> launch training -> monitor):

```
# Step 1: spawn subagent to install deps
sessions_spawn(task="Install remote dependencies...", label="step1-install")
message(action=send, text="Step 1: Installing dependencies...")
sessions_yield()

# Step 2: spawn subagent to launch training
sessions_spawn(task="Launch remote training...", label="step2-launch")
message(action=send, text="Step 2: Launching training...")
sessions_yield()

# Step 3: spawn subagent to check status
sessions_spawn(task="Check training status...", label="step3-status")
sessions_yield()
```

**Prohibited**: Executing remote SSH commands (any subcommand of `remote_train.py`) directly in the main agent via `exec`. This causes blocking with no user feedback.

### Step 1: Get Password and Verify Connection

When the user provides a password for the remote machine, **spawn a subagent** to verify the connection — don't exec directly in the main agent:

```
sessions_spawn(
  task="Verify remote connection and proceed.
    Execute command (pass password via env, do not write to files):
    exec(command='python3 scripts/remote_train.py check-connection', env={'REMOTE_SSH_PASSWORD': 'xxx'})
    Return connection result.",
  label="connect-check",
  mode="run"
)
```

### Step 2: Offer SSH Key Authentication

After a successful connection, present the following to the user (use your natural language style):

> Connected to the remote machine successfully.
>
> I recommend setting up SSH key authentication so you won't need to enter a password in the future.
>
> I'll generate an ed25519 key pair with no passphrase, so connections will be fully automatic after setup.

### Step 3: Configure Key

If the user provides a password, auto-upload the public key:
```
exec(
  command="python3 scripts/remote_train.py setup-keys --host root@... --port 37474",
  env={"REMOTE_SSH_PASSWORD": "password"}
)
```

If the user says they cannot provide a password (e.g., RunPod, cloud providers without SSH password):

1. **Ask the user** if they want to add a public key to the remote machine's management interface (e.g., RunPod SSH Keys page, AWS EC2 key pairs). Explain that this enables passwordless SSH connections.
2. If the user says yes, run `setup-keys` without a password:
   ```
   exec(command="python3 scripts/remote_train.py setup-keys --host root@... --port 37474")
   ```
3. The script will output `NO_PASSWORD_MODE` followed by the public key between `PUBLIC_KEY_START` and `PUBLIC_KEY_END` markers. Extract the public key from the output and present it to the user.
4. Instruct the user to add the public key via their cloud provider's management interface, then re-allocate/restart the instance if required.
5. After the user confirms the key has been added, run `check-connection` to verify.

If user **skips** key configuration: Continue using password. Subsequent operations still require password via environment variable.

### Subsequent Connections (Key Configured)

Connect directly, no environment variables needed:
```
exec(command="python3 scripts/remote_train.py status")
```

## Commands

```bash
# 1. Launch remote training (password via env var)
REMOTE_SSH_PASSWORD=xxx python3 scripts/remote_train.py launch \
  --host root@connect.example.com \
  --port 37474 \
  --script train_qwen25_0.5b.py \
  --log train_log.txt

# 2. Check training status (reuses ControlMaster, no password needed)
python3 scripts/remote_train.py status --tail-lines 20

# 3. Get more logs
python3 scripts/remote_train.py logs --tail-lines 100

# 4. Run a quick command on remote (for checks like nvidia-smi, free -h)
python3 scripts/remote_train.py remote-exec "nvidia-smi"

# 5. Stop if needed
python3 scripts/remote_train.py stop

# 6. Setup SSH key authentication
REMOTE_SSH_PASSWORD=xxx python3 scripts/remote_train.py setup-keys \
  --host root@connect.example.com \
  --port 37474

# 7. Check connection status
python3 scripts/remote_train.py check-connection
```

## Log Format Requirements

Training scripts must:
- Use `python3 -u` (unbuffered output)
- Redirect output to log file (`> train_log.txt 2>&1`)
- Include parseable loss/epoch info (e.g., HF Trainer JSON log format)

## Security Notes

- **Host Key Verification**: SSH connections use `StrictHostKeyChecking=no`, which skips host key verification. This is necessary for automated password-based connections (sshpass doesn't support interactive host key prompts), but exposes the connection to potential man-in-the-middle attacks. **Mitigation**: After initial setup, configure SSH key authentication and run `ssh-keyscan <host> >> ~/.ssh/known_hosts` to permanently trust the host key. Subsequent connections via ControlMaster will use the saved host key.
- **Passwords**: Passed to child processes via environment variables only, never written to any file
- **Session file**: `.remote_train_session.json` only stores non-sensitive info (host, port, pid, log path, etc.)
- **SSH ControlMaster socket**: Stored in system temp directory. Recommend periodic cleanup: `rm -rf /tmp/deepspeed_remote_ssh/`

## Session Management

`remote_train.py launch` creates `.remote_train_session.json` locally with **non-sensitive** connection info only (host, port, pid, log path). **No passwords or passphrases are ever written to this file.**

Subsequent `status`, `logs`, `stop` commands auto-read this file and reuse the ControlMaster socket — no need to repeat connection args or provide passwords.
