# Commands Cheatsheet

## Gateway

```bash
# Health check
curl -sf http://localhost:18789/health

# Restart gateway
sudo systemctl restart openclaw-gateway

# Reset after crash loop
sudo systemctl reset-failed openclaw-gateway && sudo systemctl start openclaw-gateway

# Logs
journalctl -u openclaw-gateway -f --since "5 min ago"
```

## Docker

```bash
docker ps -a                              # all containers
docker logs -f <name>                     # follow logs
docker exec -it <name> sh                 # shell in
docker system prune -a --volumes          # nuclear cleanup
docker build -t app:1.0 .                 # build
docker compose up -d                       # start stack
docker compose down                        # stop stack
```

## Git

```bash
git status                                 # working tree
git add -p                                 # interactive staging
git commit -m "type(scope): desc"          # conventional commit
git pull --rebase                          # sync without merge noise
git push --force-with-lease                # safe force push
git reflog                                 # recovery
git stash -m "wip"                         # temp save
```

## SSH

```bash
ssh -i ~/.ssh/id_ed25519 user@host        # key connect
ssh-copy-id -i ~/.ssh/id_ed25519.pub host  # deploy key
ssh -L 8080:localhost:80 host              # tunnel
ssh -A host                                # agent forwarding (trusted only)
```

## GCP

```bash
gcloud compute instances list              # list VMs
gcloud compute ssh <instance> --zone=<zone> # SSH
gcloud compute instances start <instance>  # start stopped
gcloud compute firewall-rules list         # firewall
gsutil ls gs://bucket/path                 # list GCS
gcloud secrets versions access latest --secret=<name>  # read secret
```

## Networking

```bash
ss -tulpn                                  # listening ports
ping -c 3 host                             # reachability
traceroute host                            # path
dig example.com                            # DNS
curl -v https://host:port/health           # HTTP check
sudo ufw status numbered                   # firewall rules
```

## System

```bash
df -h                                      # disk
free -m                                    # memory
top -b -n1 | head -20                     # processes
lsof +L1                                  # deleted-but-open files
systemctl list-units --failed              # failed services
sudo crontab -l                            # root cron
journalctl --vacuum-size=500M              # log cleanup
```

## Security

```bash
sudo fail2ban-client status                # ban status
sudo ufw status                            # firewall
stat -c '%a' ~/.ssh/id_ed25519             # check key perms (should be 600)
chmod 700 ~/.openclaw && chmod 600 ~/.openclaw/config.yaml  # harden
```
