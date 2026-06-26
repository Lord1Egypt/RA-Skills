---
name: tools-secops
description: >-
  Inventario de herramientas de ciberseguridad para hosts aarch64/ARM64 o x86_64 (Ubuntu 24.04+).
  Cargarlo antes de ejecutar skills comunitarias que requieran herramientas locales.
  Define rutas, uso básico y cómo invocar cada herramienta desde el agente.
metadata:
  safety: exec-authorized
  author: auditcore
  version: "1.0.0"
  openclaw: '{"emoji":"🛠️","safetyTier":"exec-authorized","tags":["tools","secops","pentest","local"]}'
---

# TOOLS-SECOPS — Inventario de Herramientas Locales

**Propósito:** Este skill define todas las herramientas de ciberseguridad instaladas
en el host local (aarch64/ARM64 o x86_64, Ubuntu 24.04+). Cargarlo cuando una
skill comunitaria necesite ejecutar comandos locales.

**Rutas base:**
- Go tools: `~/go/bin/`
- ARM64 bins: `~/tools/bin/`
- Repos git: `~/tools/`
- pip tools: `~/.local/bin/`
- Sistema: `/usr/bin/`

**Regla de ejecución:** El agente PUEDE ejecutar herramientas de reconocimiento,
análisis y escaneo. Para herramientas de explotación activa, siempre confirmar
con el operador antes de ejecutar. NUNCA ejecutar en producción sin autorización explícita.

---

## 🔍 RECONOCIMIENTO / OSINT

| Herramienta | Binario | Uso básico |
|-------------|---------|------------|
| **nmap** | `/usr/bin/nmap` | `nmap -sV -sC -p- <target>` |
| **masscan** | `/usr/bin/masscan` | `masscan <cidr> -p1-65535 --rate=1000` |
| **subfinder** | `~/go/bin/subfinder` | `subfinder -d <domain> -o subs.txt` |
| **amass** | `~/go/bin/amass` | `amass enum -passive -d <domain>` |
| **theHarvester** | `~/tools/theHarvester/theHarvester.py` | `python3 theHarvester.py -d <domain> -b all` |
| **shodan** | `~/.local/bin/shodan` | `shodan search <query>` |
| **recon-ng** | `~/tools/recon-ng/recon-ng` | `./recon-ng` (framework interactivo) |
| **dnsx** | `~/go/bin/dnsx` | `dnsx -l subs.txt -a -resp` |
| **httpx** | `~/.local/bin/httpx` | `httpx -l urls.txt -status-code -title` |

---

## 🌐 ENUMERACIÓN WEB

| Herramienta | Binario | Uso básico |
|-------------|---------|------------|
| **ffuf** | `~/go/bin/ffuf` | `ffuf -u https://<target>/FUZZ -w wordlist.txt` |
| **gobuster** | `/usr/bin/gobuster` | `gobuster dir -u <url> -w /usr/share/wordlists/dirb/common.txt` |
| **feroxbuster** | `~/tools/bin/feroxbuster` | `feroxbuster -u <url> -w wordlist.txt` |
| **whatweb** | `/usr/bin/whatweb` | `whatweb <url>` |
| **wafw00f** | `/usr/bin/wafw00f` | `wafw00f <url>` |
| **hakrawler** | `~/go/bin/hakrawler` | `echo <url> \| hakrawler` |
| **gau** | `~/go/bin/gau` | `gau <domain>` |
| **katana** | `~/go/bin/katana` | `katana -u <url> -d 3` |

---

## 🔓 ESCANEO DE VULNERABILIDADES

| Herramienta | Binario | Uso básico |
|-------------|---------|------------|
| **nuclei** | `~/go/bin/nuclei` | `nuclei -u <url> -t nuclei-templates/` |
| **nikto** | `/usr/bin/nikto` | `nikto -h <url>` |
| **wpscan** | `~/tools/wpscan/` | `ruby wpscan.rb --url <url>` |
| **joomscan** | `~/tools/joomscan/` | `perl joomscan.pl -u <url>` |
| **testssl.sh** | `~/tools/testssl.sh/testssl.sh` | `./testssl.sh <host>:<port>` |
| **sslyze** | `~/.local/bin/sslyze` | `sslyze <host>:<port>` |

---

## 💥 EXPLOTACIÓN (requiere autorización explícita del operador)

| Herramienta | Binario | Uso básico |
|-------------|---------|------------|
| **sqlmap** | `/usr/bin/sqlmap` | `sqlmap -u "<url>" --dbs` |
| **dalfox** | `~/go/bin/dalfox` | `dalfox url <url>` |
| **xsstrike** | `~/tools/XSStrike/xsstrike.py` | `python3 xsstrike.py -u <url>` |
| **commix** | `~/tools/commix/commix.py` | `python3 commix.py --url <url>` |
| **searchsploit** | `~/tools/bin/searchsploit` | `searchsploit <keyword>` |

---

## 🔑 ATAQUES A CREDENCIALES (requiere autorización del operador)

| Herramienta | Binario | Uso básico |
|-------------|---------|------------|
| **hydra** | `/usr/bin/hydra` | `hydra -l admin -P pass.txt <ip> ssh` |
| **medusa** | `/usr/bin/medusa` | `medusa -h <ip> -u admin -P pass.txt -M ssh` |
| **hashcat** | `/usr/bin/hashcat` | `hashcat -m 1000 hashes.txt wordlist.txt` |
| **john** | `/usr/sbin/john` | `john --wordlist=rockyou.txt hashes.txt` |
| **kerbrute** | `~/go/bin/kerbrute` | `kerbrute userenum -d <domain> users.txt` |
| **crackmapexec** | `~/tools/CrackMapExec/` | `python3 cme smb <ip> -u user -p pass` |

---

## 🕵️ PROXY / ANÁLISIS DE TRÁFICO

| Herramienta | Binario | Uso básico |
|-------------|---------|------------|
| **mitmproxy** | `~/.local/bin/mitmproxy` | `mitmproxy --listen-port 8080` |
| **tshark** | `/usr/bin/tshark` | `tshark -i eth0 -w capture.pcap` |
| **tcpdump** | `/usr/bin/tcpdump` | `tcpdump -i eth0 -w capture.pcap` |

---

## 🏠 POST-EXPLOTACIÓN / PIVOTING (requiere autorización)

| Herramienta | Binario | Uso básico |
|-------------|---------|------------|
| **impacket** | pip (secretsdump, smbclient, etc.) | `python3 ~/.local/bin/impacket-secretsdump <domain>/<user>@<ip>` |
| **bloodhound-python** | `~/.local/bin/bloodhound-python` | `bloodhound-python -d <domain> -u <user> -p <pass> -c all` |
| **chisel** | `~/tools/bin/chisel` | `chisel server -p 8080 --reverse` |
| **ligolo-ng** | `~/tools/bin/ligolo-ng` | `./ligolo-ng --selfcert` |
| **socat** | `/usr/bin/socat` | `socat TCP-LISTEN:4444 EXEC:/bin/bash` |

---

## ☁️ CLOUD / INFRAESTRUCTURA

| Herramienta | Binario | Uso básico |
|-------------|---------|------------|
| **pacu** | `~/.local/bin/pacu` | `pacu` (framework interactivo AWS) |
| **scoutsuite** | pip installado | `python3 -m scoutsuite aws` |
| **prowler** | `~/.local/bin/prowler` | `prowler aws --region us-east-1` |
| **trufflehog** | `~/tools/bin/trufflehog` | `trufflehog git <repo-url>` |
| **gitleaks** | `~/go/bin/gitleaks` | `gitleaks detect --source .` |

---

## 🔌 APIs / GraphQL

| Herramienta | Binario | Uso básico |
|-------------|---------|------------|
| **arjun** | `~/.local/bin/arjun` | `arjun -u <url>` |
| **kiterunner** | `~/tools/bin/kr` | `kr scan <url> -w routes-large.kite` |
| **graphw00f** | `~/tools/graphw00f/` | `python3 main.py -d -t <url>` |
| **clairvoyance** | `~/.local/bin/clairvoyance` | `clairvoyance <url>` |

---

## WORKFLOW: Cómo usar herramientas con skills comunitarias

```
1. Usuario pide: "Haz reconocimiento de ejemplo.com"
2. Agente carga: community-cybersec-index → identifica skill de reconocimiento
3. Agente carga: tools-secops → sabe qué herramientas tiene disponibles
4. Agente lee: SKILL.md de la skill comunitaria específica
5. Agente ejecuta: comandos con las herramientas locales según el workflow
6. Agente guarda: resultados en MEMORY/evidence/<assessment_id>/
```

## OUTPUTS: Dónde guardar resultados

```
MEMORY/evidence/<assessment_id>/recon/     → nmap, masscan, subfinder
MEMORY/evidence/<assessment_id>/web/       → ffuf, nikto, nuclei
MEMORY/evidence/<assessment_id>/vulns/     → nuclei, sslyze, testssl
MEMORY/evidence/<assessment_id>/creds/     → hashcat, john (hashes only)
MEMORY/evidence/<assessment_id>/cloud/     → scoutsuite, prowler, pacu
MEMORY/evidence/<assessment_id>/traffic/   → tshark, mitmproxy captures
```
