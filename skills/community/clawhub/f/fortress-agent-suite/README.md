# Fortress Agent Suite

**Fortress** is a production-grade suite for OpenClaw agents, providing self-healing, system monitoring, and proactive security hardening.

> ⚠️ **SECURITY ALERT - HIGH PRIVILEGE TOOL**
> **This suite operates with root-level access and requires a trusted environment.**
> It is designed for production Odoo/OpenClaw setups and performs autonomous system modifications (Crontab, Git, Gateway restarts, and auto-skill installation). **Do not install unless you own and trust the underlying workspace.**

---

## 🛠 Features
- 🛡️ **Self-Healing**: Automatic gateway recovery and backup restoration.
- 🩺 **Health Monitoring**: Disk, RAM, and system watchdog services.
- ⚙️ **Automated Maintenance**: Auto-cron enforcement and Git-sync for workspace integrity.
- 🤖 **Model Manager**: Autonomous management of LLM providers for 9Router.

## 🚀 Deployment Requirements
1. **Trusted Environment Only**: Only install in environments where you have full control and trust.
2. **Dependencies**: `pip install psutil`.
3. **Setup**: Apply `crontab_template.txt`.

## License
MIT
