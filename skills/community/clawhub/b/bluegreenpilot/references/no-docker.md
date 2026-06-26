# No-Docker, Script, Manual, and CI Deployments

Use this reference when deployment is not fully Docker-based.

## Discovery

Look for:

- deploy scripts;
- CI workflows;
- Makefile targets;
- SSH/runbook notes;
- service managers such as systemd, pm2, supervisor;
- reverse proxy config;
- existing rollback instructions.

## Safe Flow

1. Identify deploy command or manual steps.
2. Identify inactive slot target.
3. Verify artifact/build source.
4. Deploy to inactive slot.
5. Run healthcheck and smoke tests.
6. Ask for final switch confirmation in production.
7. Switch traffic by documented method.
8. Record state.

## Manual Switches

If switch is manual, produce exact instructions and stop before irreversible
steps. Example:

```txt
Manual switch required:
1. Point load balancer target from blue to green.
2. Keep blue running for rollback.
3. Verify public URL /health.
4. Confirm result so state can be recorded.
```

Do not claim the switch happened until the user confirms it.

