---
name: my-ip-checker
description: Get both public (external) and local (internal) IP addresses using simple shell commands. Use when the user asks for their IP, public IP, or local network address.
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["curl.exe"]}}}
---

# My IP Checker

This skill discovers both the **public (external)** IP and the **local (internal)** IP of the current machine.

## Step 1: Get public IP

Use a simple HTTPS endpoint that returns your public IP as plain text:

```bash
curl.exe -s https://ifconfig.me
```

If the service is blocked or slow, try:

```bash
curl.exe -s https://api.ipify.org
```

## Step 2: Get local IPv4 address

On **Windows** (PowerShell or cmd):

```bash
ipconfig
```

Then filter the output for lines containing `IPv4 地址` or `IPv4 Address`.

On **Linux**:

```bash
hostname -I
```

This typically returns one or more local IPs separated by spaces.

## Usage notes

- Use Step 1 when configuring firewalls, VPNs, or any external allowlist.
- Use Step 2 when debugging LAN connectivity, port forwarding, or internal routing.
- Prefer HTTPS endpoints and avoid adding API keys; these services are free and anonymous.

