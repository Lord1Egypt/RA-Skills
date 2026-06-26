# Incident Report: AllowTcpForwarding Lockout

## What happened

During SSH hardening, `AllowTcpForwarding no` was added to `/etc/ssh/sshd_config`. This immediately broke VNC tunnel access (which relies on TCP forwarding over SSH), nearly locking out the only remote access method to the VPS.

## Timeline

1. Security audit recommended disabling TCP forwarding
2. Agent applied the change and reloaded sshd
3. VNC tunnel immediately stopped working
4. User caught it because they had a second SSH session open
5. Reverted the change from the backup session

## Root cause

`AllowTcpForwarding no` prevents all SSH tunnels, including VNC-over-SSH which was the primary GUI access method.

## Lessons learned

1. **Always have a backup access method** before touching SSH config
2. **Test connectivity changes interactively** with a human watching
3. **Capture baseline state** before any network/SSH changes
4. **Never assume a "hardening" recommendation is safe** without understanding what it affects
5. **Automated rollback is essential** for unattended changes

## What we built

This incident led to the creation of the Canary Deploy skill:
- Pre-flight baseline capture
- Post-change validation
- Automatic rollback on failure
- Protocol A+B for human-in-the-loop changes

## Prevention checklist

Before any SSH/network change:
- [ ] Second SSH session open as backup
- [ ] Baseline captured (`canary-test.sh baseline`)
- [ ] Config files backed up
- [ ] Human notified and standing by
- [ ] Rollback plan documented
- [ ] Change applied and validated
