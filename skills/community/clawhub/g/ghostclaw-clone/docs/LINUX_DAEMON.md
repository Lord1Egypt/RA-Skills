# Running Ghostclaw as a Linux Daemon

If you want to run Ghostclaw's MCP Server continuously in the background on a Linux machine, you can set it up as a `systemd` service using the provided `scripts/ghostclaw.service` file.

Below are the step-by-step instructions for deploying and activating the daemon properly.

---

## 1. Prepare the Environment

The default service file assumes Ghostclaw is installed globally or in `/opt/ghostclaw`, and that a dedicated `ghostclaw` user exists for security.

### Create a dedicated service user (Optional but Recommended)

```bash
sudo useradd -r -s /bin/false ghostclaw
```

### Install the application globally

Ensure the `ghostclaw-mcp` executable is available in `/usr/local/bin` or adjust the `ExecStart` path in the `.service` file to point to your virtual environment's bin folder.

```bash
sudo pip install /path/to/ghostclaw/repo[mcp]
```

## 2. Install the Service File Automatically

The easiest way to install the daemon is to use our provided setup shell script. It will automatically detect your current Linux user (`whoami`), correctly find the `ghostclaw-mcp` path on your system, and inject these into the `.service` template.

```bash
# From the repository root, run:
./scripts/install_service.sh
```

**What this does under the hood:**

1. Replaces the generic `User=ghostclaw` with your user.
2. Replaces `WorkingDirectory=/opt/ghostclaw` with your repository root.
3. Automatically sets up `/etc/systemd/system/ghostclaw.service` utilizing `sudo`.
4. Runs `systemctl daemon-reload && systemctl enable --now ghostclaw.service`.

## 3. Manual Installation (Alternative)

If you prefer to configure the file yourself rather than running the auto-installer script:

1. Copy the file using sudo:

```bash
sudo cp scripts/ghostclaw.service /etc/systemd/system/
```

1. Manually edit `/etc/systemd/system/ghostclaw.service` and change `User=` and `WorkingDirectory=`.
2. Set permissions and start:

```bash
sudo chmod 644 /etc/systemd/system/ghostclaw.service
sudo systemctl daemon-reload
sudo systemctl enable --now ghostclaw.service
```

## 3. Enable and Start the Daemon

Once the file is in place, you need to tell systemd to reload its configuration to detect the new file, and then you can start it.

```bash
# 1. Reload systemd manager configuration
sudo systemctl daemon-reload

# 2. Enable it to start automatically on system boot
sudo systemctl enable ghostclaw.service

# 3. Start the service immediately
sudo systemctl start ghostclaw.service
```

## 4. Troubleshooting and Logs

You can check if the daemon is running properly by querying its status:

```bash
sudo systemctl status ghostclaw.service
```

If the service fails to start or crashes, view the live logs using `journalctl`:

```bash
# View the last 50 lines of logs
sudo journalctl -u ghostclaw.service -n 50 --no-pager

# Tail the logs in real-time
sudo journalctl -u ghostclaw.service -f
```
