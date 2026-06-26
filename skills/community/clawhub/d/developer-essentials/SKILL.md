---
name: developer-essentials
description: Comprehensive developer cheatsheets and quick references for Git, Docker, Kubernetes, jq, curl, and common Linux commands. Use when needing quick lookups for command syntax, common workflows, or forgotten flags for everyday developer tools.
---

# Developer Essentials Cheatsheets

Quick references for everyday developer tools. Copy-paste ready commands.

---

## 📚 Git Cheatsheet

### Basic Commands
```bash
# Initialize repo
git init

# Clone repo
git clone <url>
git clone --depth 1 <url>          # Shallow clone (faster)

# Status & info
git status
git log --oneline -n 10
git diff
git diff --staged
```

### Staging & Commits
```bash
git add .                           # Stage all
git add -p                          # Stage interactively
git commit -m "message"
git commit --amend                  # Edit last commit
git commit --amend --no-edit        # Keep message
```

### Branches
```bash
git branch                          # List branches
git branch -a                       # List all (including remote)
git checkout -b <name>              # Create & switch
git switch <name>                   # Switch branch
git merge <branch>
git rebase <branch>
```

### Push & Pull
```bash
git push origin <branch>
git push -u origin <branch>         # Set upstream
git pull
git pull --rebase
git fetch origin
```

### Undo & Fix
```bash
git restore <file>                  # Discard changes
git restore --staged <file>         # Unstage
git reset HEAD~1                    # Undo last commit (keep changes)
git reset --hard HEAD~1             # Destroy last commit
git stash
git stash pop
```

---

## 🐳 Docker Cheatsheet

### Images
```bash
docker images                       # List images
docker pull <image>
docker build -t <name> .
docker build -t <name> -f Dockerfile.dev .
docker rmi <image>
docker image prune
```

### Containers
```bash
docker ps                           # Running containers
docker ps -a                        # All containers
docker run -d -p 8080:80 <image>   # Detach + port
docker run -it --rm <image> bash    # Interactive + remove
docker exec -it <container> bash
docker logs -f <container>          # Follow logs
docker stop <container>
docker rm <container>
docker rm -f <container>            # Force remove
```

### Docker Compose
```bash
docker compose up -d
docker compose down
docker compose logs -f
docker compose restart
docker compose build
```

### Cleanup
```bash
docker system prune -a              # Remove all unused
docker system df                    # Disk usage
```

---

## ☸️ Kubernetes (kubectl) Cheatsheet

### Context & Config
```bash
kubectl config get-contexts
kubectl config use-context <name>
kubectl cluster-info
```

### Get Resources
```bash
kubectl get pods
kubectl get pods -A                 # All namespaces
kubectl get services
kubectl get deployments
kubectl get nodes
kubectl get ns                      # Namespaces
kubectl get all
```

### Describe & Debug
```bash
kubectl describe pod <pod>
kubectl logs <pod>
kubectl logs -f <pod>               # Follow
kubectl exec -it <pod> -- bash
kubectl top pods                    # Resource usage
kubectl top nodes
```

### Apply & Delete
```bash
kubectl apply -f manifest.yaml
kubectl apply -k ./                 # Kustomize
kubectl delete -f manifest.yaml
kubectl delete pod <pod>
```

### Quick Actions
```bash
kubectl expose deployment <name> --port=80 --type=LoadBalancer
kubectl scale deployment <name> --replicas=3
kubectl rollout restart deployment/<name>
```

---

## 🔍 jq Cheatsheet (JSON Processor)

### Basic Queries
```bash
# Identity (pretty print)
jq '.' file.json

# Get field
jq '.name' file.json
jq '.user.name' file.json

# Array index
jq '.[0]' file.json
jq '.[0].name' file.json
```

### Array Operations
```bash
# Array length
jq '. | length' file.json

# All items in array
jq '.[]' file.json

# Map - extract field from array
jq '.[].name' file.json
jq '.[] | {name, email}' file.json

# Filter array
jq '.[] | select(.age > 30)' file.json
jq '.[] | select(.status == "active")' file.json
```

### Transformations
```bash
# Create new object
jq '{user: .name, email: .contact.email}' file.json

# Add/remove fields
jq '. + {timestamp: now}' file.json
jq 'del(.password)' file.json
```

### Useful Flags
```bash
jq -r '.name' file.json             # Raw output (no quotes)
jq -c '.' file.json                 # Compact (one line)
jq -s '.' file1.json file2.json     # Slurp multiple files
```

---

## 🌐 curl Cheatsheet

### Basic Requests
```bash
curl https://api.example.com
curl -I https://example.com         # Headers only
curl -v https://example.com         # Verbose
```

### HTTP Methods
```bash
curl -X POST https://api.example.com/data
curl -X PUT https://api.example.com/data/1
curl -X DELETE https://api.example.com/data/1
```

### Headers & Body
```bash
curl -H "Content-Type: application/json" \
     -H "Authorization: Bearer token" \
     https://api.example.com

curl -X POST -d '{"name":"test"}' \
     -H "Content-Type: application/json" \
     https://api.example.com

curl -X POST --data @file.json https://api.example.com
```

### Output & Download
```bash
curl -o output.json https://api.example.com
curl -O https://example.com/file.zip  # Save with original name
curl -L https://example.com           # Follow redirects
```

---

## 🐧 Linux Essential Commands

### File Operations
```bash
ls -la                              # List all (including hidden)
cp -r source dest                   # Copy recursive
mv old new                          # Move/rename
rm -rf dir                          # Remove recursive force
mkdir -p path/to/dir                # Create parents too
touch file
chmod 755 file
chown user:group file
```

### Search & Find
```bash
grep "pattern" file.txt
grep -r "pattern" .                 # Recursive
grep -i "pattern" file.txt          # Case insensitive
find . -name "*.txt"
find . -type f -size +100M          # Files > 100MB
```

### Process Management
```bash
ps aux                              # All processes
top                                 # Interactive process viewer
htop                                # Better top (if installed)
kill -9 <pid>                       # Force kill
pkill -f process_name
```

### System Info
```bash
df -h                               # Disk usage
free -h                             # Memory
uname -a                            # System info
whoami
pwd                                 # Current directory
```

### Text Processing
```bash
cat file.txt
head -20 file.txt
tail -f log.txt                     # Follow file
less file.txt
wc -l file.txt                      # Line count
sort file.txt
uniq file.txt
```

### Network
```bash
ifconfig / ip addr
netstat -tulpn                      # Listening ports
ss -tulpn                           # Modern netstat
ping example.com
curl ifconfig.me                    # Get public IP
ssh user@host
scp file.txt user@host:/path
```

---

## 💡 Pro Tips

1. **Use `man <command>`** for full documentation
2. **Use `--help`** flag on most commands
3. **Pipe commands** together: `ps aux | grep nginx`
4. **History search**: Press `Ctrl+R` in terminal
5. **Aliases** save time - add to `~/.bashrc` or `~/.zshrc`
