---
name: community-cybersec-index
description: >-
  Indice Layer 0 de 754 skills comunitarias (hliosone/anthropic-cybersecurity-skills).
  Cargar junto a system-index para operaciones fuera de auditoria de red: forensics,
  malware, threat intel, IR, hunting, pentest, cloud, OT, SIEM, DevSecOps, etc.
metadata:
  safety: read-only
  author: auditcore
  version: "1.0.0"
  openclaw: '{"emoji":"shield","safetyTier":"read-only","tags":["community","layer0","cybersecurity"]}'
skills_base_path: skills/community-cybersec/skills
total_skills: 754
source: https://github.com/hliosone/anthropic-cybersecurity-skills
---

# COMMUNITY CYBERSEC INDEX — Layer 0

**Para cargar una skill:**
Leer `skills/community-cybersec/skills/{skill-id}/SKILL.md` y ejecutar su workflow.

## FORENSICS DIGITAL (63 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `acquiring-disk-image-with-dd-and-dcfldd` |  |
| `analyzing-browser-forensics-with-hindsight` |  |
| `analyzing-disk-image-with-autopsy` |  |
| `analyzing-docker-container-forensics` |  |
| `analyzing-email-headers-for-phishing-investigation` |  |
| `analyzing-heap-spray-exploitation` |  |
| `analyzing-linux-audit-logs-for-intrusion` | Uses the Linux Audit framework (auditd) with ausearch and aureport utilities to detect intrusion attempts, unauthorized   access, privilege  |
| `analyzing-linux-kernel-rootkits` |  |
| `analyzing-linux-system-artifacts` |  |
| `analyzing-lnk-file-and-jump-list-artifacts` |  |
| `analyzing-malicious-pdf-with-peepdf` |  |
| `analyzing-memory-dumps-with-volatility` | Analyzes RAM memory dumps from compromised systems using the Volatility framework to identify malicious processes,   injected code, network  |
| `analyzing-memory-forensics-with-lime-and-volatility` | Performs Linux memory acquisition using LiME (Linux Memory Extractor) kernel module and analysis with Volatility   3 framework. Extracts pro |
| `analyzing-mft-for-deleted-file-recovery` |  |
| `analyzing-outlook-pst-for-email-forensics` |  |
| `analyzing-powershell-empire-artifacts` |  |
| `analyzing-prefetch-files-for-execution-history` |  |
| `analyzing-ransomware-payment-wallets` | Traces ransomware cryptocurrency payment flows using blockchain analysis tools such as Chainalysis Reactor,   WalletExplorer, and blockchain |
| `analyzing-slack-space-and-file-system-artifacts` |  |
| `analyzing-supply-chain-malware-artifacts` |  |
| `analyzing-usb-device-connection-history` |  |
| `analyzing-windows-amcache-artifacts` | Parses and analyzes the Windows Amcache.hve registry hive to extract evidence of program execution, application   installation, and driver l |
| `analyzing-windows-lnk-files-for-artifacts` |  |
| `analyzing-windows-registry-for-artifacts` |  |
| `analyzing-windows-shellbag-artifacts` |  |
| `building-incident-timeline-with-timesketch` |  |
| `collecting-volatile-evidence-from-compromised-host` |  |
| `conducting-memory-forensics-with-volatility` | Performs memory forensics analysis using Volatility 3 to extract evidence of malware execution, process injection,   network connections, an |
| `detecting-process-injection-techniques` | Detects and analyzes process injection techniques used by malware including classic DLL injection, process hollowing,   APC injection, threa |
| `detecting-rootkit-activity` | Detects rootkit presence on compromised systems by identifying hidden processes, hooked system calls, modified   kernel structures, hidden f |
| `detecting-wmi-persistence` |  |
| `eradicating-malware-from-infected-systems` |  |
| `extracting-browser-history-artifacts` |  |
| `extracting-credentials-from-memory-dump` |  |
| `extracting-memory-artifacts-with-rekall` | Uses Rekall memory forensics framework to analyze memory dumps for process hollowing, injected code via VAD   anomalies, hidden processes, a |
| `extracting-windows-event-logs-artifacts` |  |
| `hunting-for-dcsync-attacks` |  |
| `implementing-cloud-trail-log-analysis` | Implementing AWS CloudTrail log analysis for security monitoring, threat detection, and forensic investigation   using Athena, CloudWatch Lo |
| `implementing-code-signing-for-artifacts` | This skill covers implementing code signing for build artifacts to ensure integrity and authenticity throughout   the software supply chain. |
| `implementing-velociraptor-for-ir-collection` |  |
| `investigating-ransomware-attack-artifacts` |  |
| `performing-active-directory-compromise-investigation` |  |
| `performing-cloud-forensics-investigation` |  |
| `performing-cloud-forensics-with-aws-cloudtrail` |  |
| `performing-cloud-log-forensics-with-athena` | Uses AWS Athena to query CloudTrail, VPC Flow Logs, S3 access logs, and ALB logs for forensic investigation.   Covers CREATE TABLE DDL with  |
| `performing-cloud-native-forensics-with-falco` | Uses Falco YAML rules for runtime threat detection in containers and Kubernetes, monitoring syscalls for shell   spawns, file tampering, net |
| `performing-disk-forensics-investigation` | Conducts disk forensics investigations using forensic imaging, file system analysis, artifact recovery, and   timeline reconstruction to sup |
| `performing-endpoint-forensics-investigation` | Performs digital forensics investigation on compromised endpoints including memory acquisition, disk imaging,   artifact analysis, and timel |
| `performing-file-carving-with-foremost` |  |
| `performing-insider-threat-investigation` | Investigates insider threat incidents involving employees, contractors, or trusted partners who misuse authorized   access to steal data, sa |
| `performing-linux-log-forensics-investigation` |  |
| `performing-log-analysis-for-forensic-investigation` |  |
| `performing-malware-persistence-investigation` |  |
| `performing-memory-forensics-with-volatility3` |  |
| `performing-memory-forensics-with-volatility3-plugins` |  |
| `performing-mobile-device-forensics-with-cellebrite` |  |
| `performing-network-forensics-with-wireshark` |  |
| `performing-network-traffic-analysis-with-zeek` |  |
| `performing-sqlite-database-forensics` |  |
| `performing-steganography-detection` |  |
| `performing-timeline-reconstruction-with-plaso` |  |
| `performing-windows-artifact-analysis-with-eric-zimmerman-tools` |  |
| `recovering-deleted-files-with-photorec` |  |

## MALWARE ANALYSIS (50 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `analyzing-android-malware-with-apktool` |  |
| `analyzing-bootkit-and-rootkit-samples` | Analyzes bootkit and advanced rootkit malware that infects the Master Boot Record (MBR), Volume Boot Record   (VBR), or UEFI firmware to gai |
| `analyzing-cobalt-strike-beacon-configuration` |  |
| `analyzing-cobaltstrike-malleable-c2-profiles` |  |
| `analyzing-command-and-control-communication` | Analyzes malware command-and-control (C2) communication protocols to understand beacon patterns, command structures,   data encoding, and in |
| `analyzing-golang-malware-with-ghidra` |  |
| `analyzing-linux-elf-malware` | Analyzes malicious Linux ELF (Executable and Linkable Format) binaries including botnets, cryptominers, ransomware,   and rootkits targeting |
| `analyzing-macro-malware-in-office-documents` | Analyzes malicious VBA macros embedded in Microsoft Office documents (Word, Excel, PowerPoint) to identify download   cradles, payload execu |
| `analyzing-malware-behavior-with-cuckoo-sandbox` | Executes malware samples in Cuckoo Sandbox to observe runtime behavior including process creation, file system   modifications, registry cha |
| `analyzing-malware-family-relationships-with-malpedia` |  |
| `analyzing-malware-persistence-with-autoruns` |  |
| `analyzing-malware-sandbox-evasion-techniques` |  |
| `analyzing-network-covert-channels-in-malware` |  |
| `analyzing-network-traffic-of-malware` | Analyzes network traffic generated by malware during sandbox execution or live incident response to identify   C2 protocols, data exfiltrati |
| `analyzing-packed-malware-with-upx-unpacker` | Identifies and unpacks UPX-packed and other packed malware samples to expose the original executable code for   static analysis. Covers both |
| `analyzing-pdf-malware-with-pdfid` | Analyzes malicious PDF files using PDFiD, pdf-parser, and peepdf to identify embedded JavaScript, shellcode,   exploits, and suspicious obje |
| `analyzing-ransomware-encryption-mechanisms` | Analyzes encryption algorithms, key management, and file encryption routines used by ransomware families to   assess decryption feasibility, |
| `analyzing-uefi-bootkit-persistence` | Analyzes UEFI bootkit persistence mechanisms including firmware implants in SPI flash, EFI System Partition   (ESP) modifications, Secure Bo |
| `building-automated-malware-submission-pipeline` | Builds an automated malware submission and analysis pipeline that collects suspicious files from endpoints and   email gateways, submits the |
| `building-malware-incident-communication-template` |  |
| `conducting-malware-incident-response` | Responds to malware infections across enterprise endpoints by identifying the malware family, determining infection   vectors, assessing spr |
| `deobfuscating-javascript-malware` | Deobfuscates malicious JavaScript code used in web-based attacks, phishing pages, and dropper scripts by reversing   encoding layers, eval c |
| `deobfuscating-powershell-obfuscated-malware` |  |
| `detecting-fileless-malware-techniques` | Detects and analyzes fileless malware that operates entirely in memory using PowerShell, WMI, .NET reflection,   registry-resident payloads, |
| `detecting-mobile-malware-behavior` | Detects and analyzes malicious behavior in mobile applications through behavioral analysis, permission abuse   detection, network traffic mo |
| `executing-red-team-exercise` | Executes comprehensive red team exercises that simulate real-world adversary operations against an organization |
| `extracting-iocs-from-malware-samples` | Extracts indicators of compromise (IOCs) from malware samples including file hashes, network indicators (IPs,   domains, URLs), host artifac |
| `hunting-for-cobalt-strike-beacons` |  |
| `implementing-email-sandboxing-with-proofpoint` |  |
| `implementing-semgrep-for-custom-sast-rules` |  |
| `investigating-phishing-email-incident` | Investigates phishing email incidents from initial user report through header analysis, URL/attachment detonation,   impacted user identific |
| `performing-android-app-static-analysis-with-mobsf` | Performs automated static analysis of Android applications using Mobile Security Framework (MobSF) to identify   hardcoded secrets, insecure |
| `performing-automated-malware-analysis-with-cape` |  |
| `performing-dynamic-analysis-of-android-app` | Performs runtime dynamic analysis of Android applications using Frida, Objection, and Android Debug Bridge to   observe application behavior |
| `performing-dynamic-analysis-with-any-run` | Performs interactive dynamic malware analysis using the ANY.RUN cloud sandbox to observe real-time execution   behavior, interact with malwa |
| `performing-firmware-extraction-with-binwalk` | Performs firmware image extraction and analysis using binwalk to identify embedded filesystems, compressed archives,   bootloaders, kernel i |
| `performing-firmware-malware-analysis` | Analyzes firmware images for embedded malware, backdoors, and unauthorized modifications targeting routers,   IoT devices, UEFI/BIOS, and em |
| `performing-malware-hash-enrichment-with-virustotal` |  |
| `performing-malware-ioc-extraction` |  |
| `performing-malware-triage-with-yara` | Performs rapid malware triage and classification using YARA rules to match file patterns, strings, byte sequences,   and structural characte |
| `performing-static-malware-analysis-with-pe-studio` | Performs static analysis of Windows PE (Portable Executable) malware samples using PEStudio to examine file   headers, imports, strings, res |
| `performing-threat-hunting-with-yara-rules` | Use YARA pattern-matching rules to hunt for malware, suspicious files, and indicators of compromise across filesystems   and memory dumps. C |
| `performing-yara-rule-development-for-detection` |  |
| `reverse-engineering-android-malware-with-jadx` | Reverse engineers malicious Android APK files using JADX decompiler to analyze Java/Kotlin source code, identify   malicious functionality i |
| `reverse-engineering-dotnet-malware-with-dnspy` | Reverse engineers .NET malware using dnSpy decompiler and debugger to analyze C#/VB.NET source code, identify   obfuscation techniques, extr |
| `reverse-engineering-ios-app-with-frida` | Reverse engineers iOS applications using Frida dynamic instrumentation to understand internal logic, extract   encryption keys, bypass secur |
| `reverse-engineering-malware-with-ghidra` | Reverse engineers malware binaries using NSA |
| `reverse-engineering-ransomware-encryption-routine` |  |
| `reverse-engineering-rust-malware` |  |
| `scanning-kubernetes-manifests-with-kubesec` |  |

## THREAT INTELLIGENCE (218 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `analyzing-active-directory-acl-abuse` |  |
| `analyzing-apt-group-with-mitre-navigator` |  |
| `analyzing-azure-activity-logs-for-threats` | Queries Azure Monitor activity logs and sign-in logs via azure-monitor-query to detect suspicious administrative   operations, impossible tr |
| `analyzing-campaign-attribution-evidence` |  |
| `analyzing-certificate-transparency-for-phishing` |  |
| `analyzing-indicators-of-compromise` | Analyzes indicators of compromise (IOCs) including IP addresses, domains, file hashes, URLs, and email artifacts   to determine maliciousnes |
| `analyzing-ios-app-security-with-objection` | Performs runtime mobile security exploration of iOS applications using Objection, a Frida-powered toolkit that   enables security testers to |
| `analyzing-malicious-url-with-urlscan` |  |
| `analyzing-ransomware-leak-site-intelligence` |  |
| `analyzing-threat-actor-ttps-with-mitre-attack` |  |
| `analyzing-threat-actor-ttps-with-mitre-navigator` | Map advanced persistent threat (APT) group tactics, techniques, and procedures (TTPs) to the MITRE ATT&CK framework   using the ATT&CK Navig |
| `analyzing-threat-intelligence-feeds` | Analyzes structured and unstructured threat intelligence feeds to extract actionable indicators, adversary tactics,   and campaign context.  |
| `analyzing-threat-landscape-with-misp` |  |
| `analyzing-typosquatting-domains-with-dnstwist` |  |
| `auditing-azure-active-directory-configuration` | Auditing Microsoft Entra ID (Azure Active Directory) configuration to identify risky authentication policies,   overly permissive role assig |
| `automating-ioc-enrichment` | Automates the enrichment of raw indicators of compromise with multi-source threat intelligence context using   SOAR platforms, Python pipeli |
| `building-adversary-infrastructure-tracking-system` |  |
| `building-attack-pattern-library-from-cti-reports` |  |
| `building-detection-rule-with-splunk-spl` |  |
| `building-detection-rules-with-sigma` | Builds vendor-agnostic detection rules using the Sigma rule format for threat detection across SIEM platforms   including Splunk, Elastic, a |
| `building-ioc-defanging-and-sharing-pipeline` |  |
| `building-ioc-enrichment-pipeline-with-opencti` |  |
| `building-threat-actor-profile-from-osint` |  |
| `building-threat-feed-aggregation-with-misp` |  |
| `building-threat-hunt-hypothesis-framework` |  |
| `building-threat-intelligence-enrichment-in-splunk` |  |
| `building-threat-intelligence-feed-integration` | Builds automated threat intelligence feed integration pipelines connecting STIX/TAXII feeds, open-source threat   intel, and commercial TI p |
| `building-threat-intelligence-platform` |  |
| `collecting-indicators-of-compromise` | Systematically collects, categorizes, and distributes indicators of compromise (IOCs) during and after security   incidents to enable detect |
| `collecting-open-source-intelligence` | Collects and synthesizes open-source intelligence (OSINT) about threat actors, malicious infrastructure, and   attack campaigns using public |
| `collecting-threat-intelligence-with-misp` |  |
| `conducting-api-security-testing` | Conducts security testing of REST, GraphQL, and gRPC APIs to identify vulnerabilities in authentication, authorization,   rate limiting, inp |
| `conducting-cloud-incident-response` | Responds to security incidents in cloud environments (AWS, Azure, GCP) by performing identity-based containment,   cloud-native log analysis |
| `conducting-cloud-penetration-testing` | This skill outlines methodologies for performing authorized penetration testing against AWS, Azure, and GCP   cloud environments. It covers  |
| `conducting-domain-persistence-with-dcsync` |  |
| `conducting-external-reconnaissance-with-osint` | Conducts external reconnaissance using Open Source Intelligence (OSINT) techniques to map an organization |
| `conducting-full-scope-red-team-engagement` |  |
| `conducting-internal-network-penetration-test` |  |
| `conducting-internal-reconnaissance-with-bloodhound-ce` |  |
| `conducting-man-in-the-middle-attack-simulation` | Simulates man-in-the-middle attacks using Ettercap, mitmproxy, and Bettercap in authorized environments to intercept,   analyze, and modify  |
| `conducting-mobile-app-penetration-test` | Conducts penetration testing of iOS and Android mobile applications following the OWASP Mobile Application Security   Testing Guide (MASTG)  |
| `conducting-network-penetration-test` | Conducts comprehensive network penetration tests against authorized target environments by performing host discovery,   port scanning, servi |
| `conducting-pass-the-ticket-attack` |  |
| `conducting-phishing-incident-response` | Responds to phishing incidents by analyzing reported emails, extracting indicators, assessing credential compromise,   quarantining maliciou |
| `conducting-post-incident-lessons-learned` |  |
| `conducting-social-engineering-penetration-test` |  |
| `conducting-social-engineering-pretext-call` |  |
| `conducting-spearphishing-simulation-campaign` |  |
| `conducting-wireless-network-penetration-test` | Conducts authorized wireless network penetration tests to assess the security of WiFi infrastructure by testing   for weak encryption protoc |
| `configuring-active-directory-tiered-model` |  |
| `configuring-host-based-intrusion-detection` | Configures host-based intrusion detection systems (HIDS) to monitor endpoint file integrity, system calls, and   configuration changes for s |
| `configuring-snort-ids-for-intrusion-detection` | Installs, configures, and tunes Snort 3 intrusion detection system to monitor network traffic for malicious   activity using custom and comm |
| `configuring-windows-event-logging-for-detection` | Configures Windows Event Logging with advanced audit policies to generate high-fidelity security events for   threat detection and forensic  |
| `containing-active-breach` | Executes containment strategies to stop active adversary operations and prevent lateral movement during a confirmed   security breach. Imple |
| `correlating-threat-campaigns` | Correlates disparate security incidents, IOCs, and adversary behaviors across time and organizations to identify   unified threat campaigns, |
| `deploying-active-directory-honeytokens` | Deploys deception-based honeytokens in Active Directory including fake privileged accounts with AdminCount=1,   fake SPNs for Kerberoasting  |
| `deploying-decoy-files-for-ransomware-detection` | Deploys canary files (honeytokens) across file systems to detect ransomware encryption activity in real time.   Uses strategically placed de |
| `detecting-ai-model-prompt-injection-attacks` | Detects prompt injection attacks targeting LLM-based applications using a multi-layered defense combining regex   pattern matching for known |
| `detecting-anomalies-in-industrial-control-systems` | This skill covers deploying anomaly detection systems for industrial control environments using machine learning   models trained on OT netw |
| `detecting-anomalous-authentication-patterns` | Detects anomalous authentication patterns using UEBA analytics, statistical baselines, and machine learning   models to identify impossible  |
| `detecting-api-enumeration-attacks` |  |
| `detecting-arp-poisoning-in-network-traffic` |  |
| `detecting-attacks-on-historian-servers` | Detect cyber attacks targeting OT historian servers (OSIsoft PI, Ignition, Wonderware) that sit at the IT/OT   boundary and serve as pivot p |
| `detecting-attacks-on-scada-systems` | This skill covers detecting cyber attacks targeting Supervisory Control and Data Acquisition (SCADA) systems   including man-in-the-middle a |
| `detecting-aws-cloudtrail-anomalies` |  |
| `detecting-aws-credential-exposure-with-trufflehog` | Detecting exposed AWS credentials in source code repositories, CI/CD pipelines, and configuration files using   TruffleHog, git-secrets, and |
| `detecting-aws-guardduty-findings-automation` |  |
| `detecting-aws-iam-privilege-escalation` |  |
| `detecting-azure-lateral-movement` |  |
| `detecting-azure-service-principal-abuse` |  |
| `detecting-azure-storage-account-misconfigurations` |  |
| `detecting-beaconing-patterns-with-zeek` | Performs statistical analysis of Zeek conn.log connection intervals to detect C2 beaconing patterns. Uses the   ZAT library to load Zeek log |
| `detecting-bluetooth-low-energy-attacks` | Detects and analyzes Bluetooth Low Energy (BLE) security attacks including sniffing, replay attacks, GATT enumeration   abuse, and Man-in-th |
| `detecting-broken-object-property-level-authorization` |  |
| `detecting-business-email-compromise` |  |
| `detecting-business-email-compromise-with-ai` |  |
| `detecting-cloud-threats-with-guardduty` | This skill teaches security teams how to deploy and operationalize Amazon GuardDuty for continuous threat detection   across AWS accounts an |
| `detecting-command-and-control-over-dns` | Detects command-and-control (C2) communications tunneled through DNS protocol including DNS tunneling tools   (Iodine, dnscat2, dns2tcp, Cob |
| `detecting-compromised-cloud-credentials` | Detecting compromised cloud credentials across AWS, Azure, and GCP by analyzing anomalous API activity, impossible   travel patterns, unauth |
| `detecting-container-drift-at-runtime` |  |
| `detecting-container-escape-attempts` |  |
| `detecting-container-escape-with-falco-rules` |  |
| `detecting-credential-dumping-techniques` |  |
| `detecting-cryptomining-in-cloud` | This skill teaches security teams how to detect and respond to unauthorized cryptocurrency mining operations   in cloud environments. It cov |
| `detecting-dcsync-attack-in-active-directory` |  |
| `detecting-deepfake-audio-in-vishing-attacks` | Detects AI-generated deepfake audio used in voice phishing (vishing) attacks by extracting spectral features   (MFCC, spectral centroid, spe |
| `detecting-dll-sideloading-attacks` |  |
| `detecting-dnp3-protocol-anomalies` | Detect anomalies in DNP3 (Distributed Network Protocol 3) communications used in SCADA systems by monitoring   for unauthorized control comm |
| `detecting-dns-exfiltration-with-dns-query-analysis` |  |
| `detecting-email-account-compromise` |  |
| `detecting-email-forwarding-rules-attack` |  |
| `detecting-evasion-techniques-in-endpoint-logs` | Detects defense evasion techniques used by adversaries in endpoint logs including log tampering, timestomping,   process injection, and secu |
| `detecting-exfiltration-over-dns-with-zeek` |  |
| `detecting-fileless-attacks-on-endpoints` | Detects fileless malware and in-memory attacks that execute entirely in RAM without writing persistent files   to disk, evading traditional  |
| `detecting-golden-ticket-attacks-in-kerberos-logs` |  |
| `detecting-golden-ticket-forgery` |  |
| `detecting-insider-data-exfiltration-via-dlp` | Detects insider data exfiltration by analyzing DLP policy violations, file access patterns, upload volume anomalies,   and off-hours activit |
| `detecting-insider-threat-behaviors` |  |
| `detecting-insider-threat-with-ueba` |  |
| `detecting-kerberoasting-attacks` |  |
| `detecting-lateral-movement-in-network` | Identifies lateral movement techniques in enterprise networks by analyzing authentication logs, network flows,   SMB traffic, and RDP sessio |
| `detecting-lateral-movement-with-splunk` |  |
| `detecting-lateral-movement-with-zeek` | Detect lateral movement in network traffic using Zeek (formerly Bro) log analysis. Parses conn.log, smb_mapping.log,   smb_files.log, dce_rp |
| `detecting-living-off-the-land-attacks` | Detect abuse of legitimate Windows binaries (LOLBins) used for living off the land attacks. Monitors process   creation, command-line argume |
| `detecting-living-off-the-land-with-lolbas` |  |
| `detecting-malicious-scheduled-tasks-with-sysmon` | Detect malicious scheduled task creation and modification using Sysmon Event IDs 1 (Process Create for schtasks.exe),   11 (File Create for  |
| `detecting-mimikatz-execution-patterns` |  |
| `detecting-misconfigured-azure-storage` | Detecting misconfigured Azure Storage accounts including publicly accessible blob containers, missing encryption   settings, overly permissi |
| `detecting-modbus-command-injection-attacks` | Detect command injection attacks against Modbus TCP/RTU protocol in ICS environments by monitoring for unauthorized   write operations, anom |
| `detecting-modbus-protocol-anomalies` | This skill covers detecting anomalies in Modbus/TCP and Modbus RTU communications in industrial control systems.   It addresses function cod |
| `detecting-network-anomalies-with-zeek` | Deploys and configures Zeek (formerly Bro) network security monitor to passively analyze network traffic, generate   structured logs, detect |
| `detecting-network-scanning-with-ids-signatures` |  |
| `detecting-ntlm-relay-with-event-correlation` | Detect NTLM relay attacks through Windows Security Event correlation by analyzing Event 4624 LogonType 3 for   IP-to-hostname mismatches, id |
| `detecting-oauth-token-theft` | Detects and responds to OAuth token theft and replay attacks in cloud environments, focusing on Microsoft Entra   ID (Azure AD) token protec |
| `detecting-pass-the-hash-attacks` |  |
| `detecting-pass-the-ticket-attacks` |  |
| `detecting-port-scanning-with-fail2ban` | Configures Fail2ban with custom filters and actions to detect port scanning activity, SSH brute force attempts,   and network reconnaissance |
| `detecting-privilege-escalation-attempts` |  |
| `detecting-privilege-escalation-in-kubernetes-pods` |  |
| `detecting-process-hollowing-technique` |  |
| `detecting-qr-code-phishing-with-email-security` |  |
| `detecting-ransomware-encryption-behavior` | Detects ransomware encryption activity in real time using entropy analysis, file system I/O monitoring, and   behavioral heuristics. Identif |
| `detecting-ransomware-precursors-in-network` | Detects early-stage ransomware indicators in network traffic before encryption begins, including initial access   broker activity, command-a |
| `detecting-rdp-brute-force-attacks` |  |
| `detecting-s3-data-exfiltration-attempts` | Detecting data exfiltration attempts from AWS S3 buckets by analyzing CloudTrail S3 data events, VPC Flow Logs,   GuardDuty findings, Amazon |
| `detecting-serverless-function-injection` | Detects and prevents code injection attacks targeting serverless functions (AWS Lambda, Azure Functions, Google   Cloud Functions) through e |
| `detecting-service-account-abuse` |  |
| `detecting-shadow-api-endpoints` |  |
| `detecting-shadow-it-cloud-usage` |  |
| `detecting-spearphishing-with-email-gateway` |  |
| `detecting-sql-injection-via-waf-logs` |  |
| `detecting-stuxnet-style-attacks` | This skill covers detecting sophisticated cyber-physical attacks that follow the Stuxnet attack pattern of modifying   PLC logic while spoof |
| `detecting-supply-chain-attacks-in-ci-cd` | Scans GitHub Actions workflows and CI/CD pipeline configurations for supply chain attack vectors including unpinned   actions, script inject |
| `detecting-suspicious-oauth-application-consent` |  |
| `detecting-suspicious-powershell-execution` |  |
| `detecting-t1003-credential-dumping-with-edr` |  |
| `detecting-t1055-process-injection-with-sysmon` |  |
| `detecting-t1548-abuse-elevation-control-mechanism` |  |
| `detecting-typosquatting-packages-in-npm-pypi` | Detects typosquatting attacks in npm and PyPI package registries by analyzing package name similarity using   Levenshtein distance and other |
| `evaluating-threat-intelligence-platforms` | Evaluates and selects Threat Intelligence Platform (TIP) products based on organizational requirements including   feed integration capabili |
| `executing-active-directory-attack-simulation` | Executes authorized attack simulations against Active Directory environments to identify misconfigurations,   weak credentials, dangerous pr |
| `exploiting-active-directory-certificate-services-esc1` |  |
| `exploiting-active-directory-with-bloodhound` |  |
| `exploiting-api-injection-vulnerabilities` | Tests APIs for injection vulnerabilities including SQL injection, NoSQL injection, OS command injection, LDAP   injection, and Server-Side R |
| `exploiting-broken-function-level-authorization` | Tests APIs for Broken Function Level Authorization (BFLA) vulnerabilities where regular users can invoke administrative   functions or acces |
| `exploiting-nosql-injection-vulnerabilities` |  |
| `exploiting-sql-injection-vulnerabilities` | Identifies and exploits SQL injection vulnerabilities in web applications during authorized penetration tests   using manual techniques and  |
| `exploiting-sql-injection-with-sqlmap` |  |
| `exploiting-template-injection-vulnerabilities` |  |
| `extracting-config-from-agent-tesla-rat` |  |
| `generating-threat-intelligence-reports` | Generates structured cyber threat intelligence reports at strategic, operational, and tactical levels tailored   to specific audiences inclu |
| `hardening-docker-containers-for-production` |  |
| `hunting-for-process-injection-techniques` |  |
| `hunting-for-unusual-network-connections` |  |
| `hunting-for-webshell-activity` |  |
| `implementing-alert-fatigue-reduction` | Implements strategies to reduce SOC alert fatigue by tuning detection rules, consolidating duplicate alerts,   implementing risk-based alert |
| `implementing-api-abuse-detection-with-rate-limiting` |  |
| `implementing-api-threat-protection-with-apigee` |  |
| `implementing-cloud-dlp-for-data-protection` | Implementing Cloud Data Loss Prevention (DLP) using Amazon Macie, Azure Information Protection, and Google Cloud   DLP API to discover, clas |
| `implementing-cloud-workload-protection` | Implements cloud workload protection using boto3 and google-cloud APIs for runtime security monitoring, process   anomaly detection, and fil |
| `implementing-deception-based-detection-with-canarytoken` |  |
| `implementing-diamond-model-analysis` |  |
| `implementing-dragos-platform-for-ot-monitoring` | Deploy and configure the Dragos Platform for OT network monitoring, leveraging its 600+ industrial protocol   parsers, intelligence-driven t |
| `implementing-endpoint-detection-with-wazuh` |  |
| `implementing-gdpr-data-protection-controls` |  |
| `implementing-google-workspace-phishing-protection` |  |
| `implementing-honeypot-for-ransomware-detection` | Deploys canary files, honeypot shares, and decoy systems to detect ransomware activity at the earliest possible   stage. Configures canary t |
| `implementing-honeytokens-for-breach-detection` | Deploys canary tokens and honeytokens (fake AWS credentials, DNS canaries, document beacons, database records)   that trigger alerts when ac |
| `implementing-memory-protection-with-dep-aslr` | Implements memory protection mechanisms including DEP (Data Execution Prevention), ASLR (Address Space Layout   Randomization), CFG (Control |
| `implementing-mimecast-targeted-attack-protection` |  |
| `implementing-ransomware-kill-switch-detection` | Detects and exploits ransomware kill switch mechanisms including mutex-based execution guards, domain-based   kill switches, and registry-ba |
| `implementing-runtime-application-self-protection` |  |
| `implementing-security-information-sharing-with-stix2` | Create, validate, and share STIX 2.1 threat intelligence objects using the stix2 Python library. Covers indicators,   malware, campaigns, re |
| `implementing-siem-use-cases-for-detection` | Implements SIEM detection use cases by designing correlation rules, threshold alerts, and behavioral analytics   mapped to MITRE ATT&CK tech |
| `implementing-stix-taxii-feed-integration` |  |
| `implementing-taxii-server-with-opentaxii` |  |
| `implementing-threat-intelligence-lifecycle-management` |  |
| `integrating-sast-into-github-actions-pipeline` | This skill covers integrating Static Application Security Testing (SAST) tools—CodeQL and Semgrep—into GitHub   Actions CI/CD pipelines. It  |
| `managing-intelligence-lifecycle` | Manages the end-to-end cyber threat intelligence lifecycle from planning and direction through collection, processing,   analysis, dissemina |
| `monitoring-darkweb-sources` | Monitors dark web forums, marketplaces, paste sites, and ransomware leak sites for mentions of organizational   assets, leaked credentials,  |
| `performing-active-directory-bloodhound-analysis` |  |
| `performing-active-directory-forest-trust-attack` |  |
| `performing-active-directory-penetration-test` |  |
| `performing-active-directory-vulnerability-assessment` |  |
| `performing-adversary-in-the-middle-phishing-detection` |  |
| `performing-ai-driven-osint-correlation` |  |
| `performing-brand-monitoring-for-impersonation` |  |
| `performing-cloud-native-threat-hunting-with-aws-detective` |  |
| `performing-container-escape-detection` | Detects container escape attempts by analyzing namespace configurations, privileged container checks, dangerous   capability assignments, an |
| `performing-cve-prioritization-with-kev-catalog` |  |
| `performing-dark-web-monitoring-for-threats` |  |
| `performing-dns-tunneling-detection` | Detects DNS tunneling by computing Shannon entropy of DNS query names, analyzing query length distributions,   inspecting TXT record payload |
| `performing-false-positive-reduction-in-siem` |  |
| `performing-graphql-introspection-attack` | Performs GraphQL introspection attacks to extract the full API schema including types, queries, mutations, subscriptions,   and field defini |
| `performing-indicator-lifecycle-management` |  |
| `performing-ioc-enrichment-automation` | Automates Indicator of Compromise (IOC) enrichment by orchestrating lookups across VirusTotal, AbuseIPDB, Shodan,   MISP, and other intellig |
| `performing-ip-reputation-analysis-with-shodan` |  |
| `performing-lateral-movement-detection` | Detects lateral movement techniques including Pass-the-Hash, PsExec, WMI execution, RDP pivoting, and SMB-based   spreading using SIEM corre |
| `performing-open-source-intelligence-gathering` |  |
| `performing-osint-with-spiderfoot` |  |
| `performing-packet-injection-attack` | Crafts and injects custom network packets using Scapy, hping3, and Nemesis during authorized security assessments   to test firewall rules,  |
| `performing-paste-site-monitoring-for-credentials` |  |
| `performing-second-order-sql-injection` |  |
| `performing-serverless-function-security-review` | Performing security reviews of serverless functions across AWS Lambda, Azure Functions, and GCP Cloud Functions   to identify overly permiss |
| `performing-ssl-tls-inspection-configuration` |  |
| `performing-subdomain-enumeration-with-subfinder` |  |
| `performing-supply-chain-attack-simulation` |  |
| `performing-threat-intelligence-sharing-with-misp` |  |
| `performing-threat-landscape-assessment-for-sector` |  |
| `processing-stix-taxii-feeds` | Processes STIX 2.1 threat intelligence bundles delivered via TAXII 2.1 servers, normalizing objects into platform-native   schemas and routi |
| `profiling-threat-actor-groups` | Develops comprehensive threat actor profiles for APT groups, criminal organizations, and hacktivist collectives   by aggregating TTP documen |
| `securing-github-actions-workflows` | This skill covers hardening GitHub Actions workflows against supply chain attacks, credential theft, and privilege   escalation. It addresse |
| `securing-serverless-functions` | This skill covers security hardening for serverless compute platforms including AWS Lambda, Azure Functions,   and Google Cloud Functions. I |
| `testing-for-email-header-injection` |  |
| `testing-for-host-header-injection` |  |
| `testing-for-xml-injection-vulnerabilities` |  |
| `testing-for-xxe-injection-vulnerabilities` |  |
| `tracking-threat-actor-infrastructure` |  |

## INCIDENT RESPONSE (35 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `analyzing-network-traffic-with-wireshark` | Captures and analyzes network packet data using Wireshark and tshark to identify malicious traffic patterns,   diagnose protocol issues, ext |
| `analyzing-persistence-mechanisms-in-linux` |  |
| `analyzing-windows-prefetch-with-python` |  |
| `building-incident-response-dashboard` | Builds real-time incident response dashboards in Splunk, Elastic, or Grafana to provide SOC analysts and leadership   with situational aware |
| `building-incident-response-playbook` | Designs and documents structured incident response playbooks that define step-by-step procedures for specific   incident types aligned with  |
| `building-phishing-reporting-button-workflow` |  |
| `building-ransomware-playbook-with-cisa-framework` | Builds a structured ransomware incident response playbook aligned with the CISA StopRansomware Guide and NIST   Cybersecurity Framework. Cov |
| `building-soc-playbook-for-ransomware` | Builds a structured SOC incident response playbook for ransomware attacks covering detection, containment, eradication,   and recovery phase |
| `configuring-pfsense-firewall-rules` | Configures pfSense firewall rules, NAT policies, VPN tunnels, and traffic shaping to enforce network segmentation,   control traffic flow, a |
| `implementing-gcp-vpc-firewall-rules` | Implementing and auditing GCP VPC firewall rules to enforce network segmentation, restrict ingress and egress   traffic, apply hierarchical  |
| `implementing-ics-firewall-with-tofino` | Deploy and configure Tofino industrial firewalls from Belden/Hirschmann to protect SCADA systems and PLCs using   deep packet inspection for |
| `implementing-network-segmentation-with-firewall-zones` |  |
| `implementing-next-generation-firewall-with-palo-alto` |  |
| `implementing-ot-incident-response-playbook` | Develop and implement OT-specific incident response playbooks aligned with SANS PICERL framework, IEC 62443,   and NIST SP 800-82 that addre |
| `implementing-ransomware-backup-strategy` | Designs and implements a ransomware-resilient backup strategy following the 3-2-1-1-0 methodology (3 copies,   2 media types, 1 offsite, 1 i |
| `implementing-rsa-key-pair-management` |  |
| `implementing-soar-automation-with-phantom` | Implements Security Orchestration, Automation, and Response (SOAR) workflows using Splunk SOAR (formerly Phantom)   to automate alert triage |
| `implementing-soar-playbook-for-phishing` |  |
| `implementing-soar-playbook-with-palo-alto-xsoar` |  |
| `performing-cloud-incident-containment-procedures` |  |
| `performing-directory-traversal-testing` |  |
| `performing-plc-firmware-security-analysis` | This skill covers analyzing Programmable Logic Controller (PLC) firmware for security vulnerabilities including   hardcoded credentials, ins |
| `performing-ransomware-tabletop-exercise` | Plans and facilitates tabletop exercises simulating ransomware incidents to test organizational readiness, decision-making,   and communicat |
| `performing-soc-tabletop-exercise` | Performs tabletop exercises for SOC teams simulating security incidents through discussion-based scenarios to   test incident response proce |
| `performing-web-application-firewall-bypass` |  |
| `performing-wifi-password-cracking-with-aircrack` | Captures WPA/WPA2 handshakes and performs offline password cracking using aircrack-ng, hashcat, and dictionary   attacks during authorized w |
| `performing-wireless-network-penetration-test` |  |
| `performing-wireless-security-assessment-with-kismet` |  |
| `recovering-from-ransomware-attack` | Executes structured recovery from a ransomware incident following NIST and CISA frameworks, including environment   isolation, forensic evid |
| `securing-historian-server-in-ot-environment` | This skill covers hardening and securing process historian servers (OSIsoft PI, Honeywell PHD, GE Proficy, AVEVA   Historian) in OT environm |
| `securing-remote-access-to-ot-environment` | This skill covers implementing secure remote access to OT/ICS environments for operators, engineers, and vendors   while preventing unauthor |
| `testing-for-open-redirect-vulnerabilities` |  |
| `testing-ransomware-recovery-procedures` |  |
| `triaging-security-incident-with-ir-playbook` |  |
| `validating-backup-integrity-for-recovery` |  |

## THREAT HUNTING (31 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `deploying-osquery-for-endpoint-monitoring` | Deploys and configures osquery for real-time endpoint monitoring using SQL-based queries to inspect running   processes, open ports, install |
| `hunting-advanced-persistent-threats` | Proactively hunts for Advanced Persistent Threat (APT) activity within enterprise environments using hypothesis-driven   searches across end |
| `hunting-credential-stuffing-attacks` | Detects credential stuffing attacks by analyzing authentication logs for login velocity anomalies, ASN diversity,   password spray patterns, |
| `hunting-for-anomalous-powershell-execution` | Hunt for malicious PowerShell activity by analyzing Script Block Logging (Event 4104), Module Logging (Event   4103), and process creation e |
| `hunting-for-beaconing-with-frequency-analysis` |  |
| `hunting-for-command-and-control-beaconing` |  |
| `hunting-for-data-exfiltration-indicators` |  |
| `hunting-for-data-staging-before-exfiltration` |  |
| `hunting-for-dcom-lateral-movement` | Hunt for DCOM-based lateral movement by detecting abuse of MMC20.Application, ShellBrowserWindow, and ShellWindows   COM objects through Sys |
| `hunting-for-defense-evasion-via-timestomping` | Detect NTFS timestamp manipulation (MITRE T1070.006) by comparing $STANDARD_INFORMATION vs $FILE_NAME timestamps   in the MFT. Uses analyzeM |
| `hunting-for-dns-based-persistence` |  |
| `hunting-for-dns-tunneling-with-zeek` |  |
| `hunting-for-domain-fronting-c2-traffic` |  |
| `hunting-for-lateral-movement-via-wmi` |  |
| `hunting-for-living-off-the-cloud-techniques` |  |
| `hunting-for-living-off-the-land-binaries` |  |
| `hunting-for-lolbins-execution-in-endpoint-logs` |  |
| `hunting-for-ntlm-relay-attacks` |  |
| `hunting-for-persistence-mechanisms-in-windows` |  |
| `hunting-for-persistence-via-wmi-subscriptions` |  |
| `hunting-for-registry-persistence-mechanisms` |  |
| `hunting-for-registry-run-key-persistence` |  |
| `hunting-for-scheduled-task-persistence` |  |
| `hunting-for-shadow-copy-deletion` |  |
| `hunting-for-spearphishing-indicators` |  |
| `hunting-for-startup-folder-persistence` |  |
| `hunting-for-supply-chain-compromise` |  |
| `hunting-for-suspicious-scheduled-tasks` |  |
| `hunting-for-t1098-account-manipulation` |  |
| `hunting-for-unusual-service-installations` |  |
| `performing-threat-hunting-with-elastic-siem` | Performs proactive threat hunting in Elastic Security SIEM using KQL/EQL queries, detection rules, and Timeline   investigation to identify  |

## SIEM / DETECTION (17 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `analyzing-dns-logs-for-exfiltration` | Analyzes DNS query logs to detect data exfiltration via DNS tunneling, DGA domain communication, and covert   C2 channels using entropy anal |
| `analyzing-security-logs-with-splunk` | Leverages Splunk Enterprise Security and SPL (Search Processing Language) to investigate security incidents   through log correlation, timel |
| `analyzing-windows-event-logs-in-splunk` | Analyzes Windows Security, System, and Sysmon event logs in Splunk to detect authentication attacks, privilege   escalation, persistence mec |
| `building-cloud-siem-with-sentinel` | This skill covers deploying Microsoft Sentinel as a cloud-native SIEM and SOAR platform for centralized security   operations. It details co |
| `correlating-security-events-in-qradar` | Correlates security events in IBM QRadar SIEM using AQL (Ariel Query Language), custom rules, building blocks,   and offense management to d |
| `deploying-ransomware-canary-files` | Deploys and monitors ransomware canary files across critical directories using Python |
| `implementing-log-forwarding-with-fluentd` |  |
| `implementing-network-deception-with-honeypots` |  |
| `implementing-security-monitoring-with-datadog` | Implements security monitoring using Datadog Cloud SIEM, Cloud Security Management (CSM), and Workload Protection   to detect threats, enfor |
| `implementing-siem-correlation-rules-for-apt` |  |
| `implementing-siem-use-case-tuning` |  |
| `mapping-mitre-attack-techniques` | Maps observed adversary behaviors, security alerts, and detection rules to MITRE ATT&CK techniques and sub-techniques   to quantify detectio |
| `performing-alert-triage-with-elastic-siem` |  |
| `performing-deception-technology-deployment` | Deploys deception technology including honeypots, honeytokens, and decoy systems to detect attackers who have   bypassed perimeter defenses, |
| `performing-log-source-onboarding-in-siem` |  |
| `performing-user-behavior-analytics` | Performs User and Entity Behavior Analytics (UEBA) to detect anomalous user activities including impossible   travel, unusual access pattern |
| `triaging-security-alerts-in-splunk` | Triages security alerts in Splunk Enterprise Security by classifying severity, investigating notable events,   correlating related telemetry |

## NETWORK SECURITY (30 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `analyzing-network-flow-data-with-netflow` |  |
| `analyzing-network-packets-with-scapy` |  |
| `analyzing-network-traffic-for-incidents` | Analyzes network traffic captures and flow data to identify adversary activity during security incidents, including   command-and-control co |
| `analyzing-ransomware-network-indicators` |  |
| `configuring-microsegmentation-for-zero-trust` |  |
| `configuring-network-segmentation-with-vlans` | Designs and implements VLAN-based network segmentation on managed switches to isolate network zones, enforce   access control between segmen |
| `configuring-suricata-for-network-monitoring` | Deploys and configures Suricata IDS/IPS with Emerging Threats rulesets, EVE JSON logging, and custom rules for   real-time network traffic i |
| `configuring-tls-1-3-for-secure-communications` |  |
| `exploiting-bgp-hijacking-vulnerabilities` | Analyzes and simulates BGP hijacking scenarios in authorized lab environments to assess route origin validation,   RPKI deployment, and BGP  |
| `exploiting-ipv6-vulnerabilities` | Identifies and exploits IPv6-specific vulnerabilities including SLAAC spoofing, Router Advertisement flooding,   and IPv6 tunneling during a |
| `exploiting-smb-vulnerabilities-with-metasploit` | Identifies and exploits SMB protocol vulnerabilities using Metasploit Framework during authorized penetration   tests to demonstrate risks f |
| `implementing-bgp-security-with-rpki` |  |
| `implementing-canary-tokens-for-network-intrusion` | Deploys DNS, HTTP, and AWS API key canary tokens across network infrastructure to detect unauthorized access   and lateral movement. Integra |
| `implementing-ddos-mitigation-with-cloudflare` |  |
| `implementing-network-access-control` | Implements 802.1X port-based network access control using RADIUS authentication, PacketFence NAC, and switch   configurations to enforce ide |
| `implementing-network-access-control-with-cisco-ise` |  |
| `implementing-network-intrusion-prevention-with-suricata` |  |
| `implementing-network-traffic-baselining` |  |
| `performing-arp-spoofing-attack-simulation` | Simulates ARP spoofing attacks in authorized lab or pentest environments using arpspoof, Ettercap, and Scapy   to demonstrate man-in-the-mid |
| `performing-authenticated-scan-with-openvas` |  |
| `performing-bandwidth-throttling-attack-simulation` | Simulates bandwidth throttling and network degradation attacks using tc, iperf3, and Scapy in authorized environments   to test quality-of-s |
| `performing-dns-enumeration-and-zone-transfer` | Enumerates DNS records, attempts zone transfers, brute-forces subdomains, and maps DNS infrastructure during   authorized reconnaissance to  |
| `performing-external-network-penetration-test` |  |
| `performing-network-packet-capture-analysis` |  |
| `performing-network-traffic-analysis-with-tshark` |  |
| `performing-ot-network-security-assessment` | This skill covers conducting comprehensive security assessments of Operational Technology (OT) networks including   SCADA systems, DCS archi |
| `performing-ssl-stripping-attack` | Simulates SSL stripping attacks using sslstrip, Bettercap, and mitmproxy in authorized environments to test   HSTS enforcement, certificate  |
| `performing-ssl-tls-security-assessment` |  |
| `performing-vlan-hopping-attack` | Simulates VLAN hopping attacks using switch spoofing and double tagging techniques in authorized environments   to test VLAN segmentation ef |
| `scanning-network-with-nmap-advanced` | Performs advanced network reconnaissance using Nmap |

## CLOUD SECURITY (42 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `analyzing-cloud-storage-access-patterns` |  |
| `auditing-aws-s3-bucket-permissions` | Systematically audit AWS S3 bucket permissions to identify publicly accessible buckets, overly permissive ACLs,   misconfigured bucket polic |
| `auditing-cloud-with-cis-benchmarks` | This skill details how to conduct cloud security audits using Center for Internet Security benchmarks for AWS,   Azure, and GCP. It covers i |
| `auditing-gcp-iam-permissions` | Auditing Google Cloud Platform IAM permissions to identify overly permissive bindings, primitive role usage,   service account key prolifera |
| `auditing-terraform-infrastructure-for-security` | Auditing Terraform infrastructure-as-code for security misconfigurations using Checkov, tfsec, Terrascan, and   OPA/Rego policies to detect  |
| `building-identity-federation-with-saml-azure-ad` |  |
| `configuring-aws-verified-access-for-ztna` |  |
| `configuring-identity-aware-proxy-with-google-iap` | Configuring Google Cloud Identity-Aware Proxy (IAP) to enforce per-request identity verification for Compute   Engine, App Engine, Cloud Run |
| `deploying-cloudflare-access-for-zero-trust` | Deploying Cloudflare Access with Cloudflare Tunnel to provide zero trust access to self-hosted and private applications,   configuring ident |
| `implementing-aws-config-rules-for-compliance` | Implementing AWS Config rules for continuous compliance monitoring of AWS resources, deploying managed and custom   rules aligned to CIS and |
| `implementing-aws-iam-permission-boundaries` |  |
| `implementing-aws-macie-for-data-classification` |  |
| `implementing-aws-nitro-enclave-security` | Implements AWS Nitro Enclave-based confidential computing environments with cryptographic attestation, KMS policy   integration using PCR-ba |
| `implementing-aws-security-hub` | This skill covers deploying AWS Security Hub as a centralized cloud security posture management platform that   aggregates findings from Gua |
| `implementing-aws-security-hub-compliance` | Implementing AWS Security Hub to aggregate security findings across AWS accounts, enable compliance standards   like CIS AWS Foundations and |
| `implementing-azure-ad-privileged-identity-management` |  |
| `implementing-azure-defender-for-cloud` | Implementing Microsoft Defender for Cloud to enable cloud security posture management, workload protection across   VMs, containers, databas |
| `implementing-cloud-security-posture-management` | Implementing Cloud Security Posture Management (CSPM) to continuously monitor multi-cloud environments for misconfigurations,   compliance v |
| `implementing-cloud-vulnerability-posture-management` |  |
| `implementing-cloud-waf-rules` | This skill covers deploying and tuning Web Application Firewall rules on AWS WAF, Azure WAF, and Cloudflare   to protect cloud-hosted applic |
| `implementing-conditional-access-policies-azure-ad` |  |
| `implementing-envelope-encryption-with-aws-kms` |  |
| `implementing-gcp-binary-authorization` |  |
| `implementing-gcp-organization-policy-constraints` |  |
| `implementing-immutable-backup-with-restic` | Implements immutable backup strategy using restic with S3-compatible storage and object lock for ransomware-resistant   data protection. Aut |
| `implementing-infrastructure-as-code-security-scanning` | This skill covers implementing automated security scanning for Infrastructure as Code (IaC) templates using   tools like Checkov, tfsec, and |
| `implementing-zero-trust-in-cloud` | This skill guides organizations through implementing zero trust architecture in cloud environments following   NIST SP 800-207 and Google Be |
| `managing-cloud-identity-with-okta` | This skill covers implementing Okta as a centralized identity provider for cloud environments, configuring SSO   integration with AWS, Azure |
| `performing-aws-account-enumeration-with-scout-suite` |  |
| `performing-aws-privilege-escalation-assessment` | Performing authorized privilege escalation assessments in AWS environments to identify IAM misconfigurations   that allow users or roles to  |
| `performing-cloud-asset-inventory-with-cartography` |  |
| `performing-cloud-penetration-testing-with-pacu` | Performing authorized AWS penetration testing using Pacu, the open-source AWS exploitation framework, to enumerate   IAM configurations, dis |
| `performing-cloud-storage-forensic-acquisition` |  |
| `performing-gcp-penetration-testing-with-gcpbucketbrute` |  |
| `performing-gcp-security-assessment-with-forseti` | Performing comprehensive security assessments of Google Cloud Platform environments using Forseti Security,   Security Command Center, and g |
| `remediating-s3-bucket-misconfiguration` | This skill provides step-by-step procedures for identifying and remediating Amazon S3 bucket misconfigurations   that expose sensitive data  |
| `securing-api-gateway-with-aws-waf` | Securing API Gateway endpoints with AWS WAF by configuring managed rule groups for OWASP Top 10 protection,   creating custom rate limiting  |
| `securing-aws-iam-permissions` | This skill guides practitioners through hardening AWS Identity and Access Management configurations to enforce   least privilege access acro |
| `securing-aws-lambda-execution-roles` | Securing AWS Lambda execution roles by implementing least-privilege IAM policies, applying permission boundaries,   restricting resource-bas |
| `securing-azure-with-microsoft-defender` | This skill instructs security practitioners on deploying Microsoft Defender for Cloud as a cloud-native application   protection platform fo |
| `securing-kubernetes-on-cloud` | This skill covers hardening managed Kubernetes clusters on EKS, AKS, and GKE by implementing Pod Security Standards,   network policies, wor |
| `testing-oauth2-implementation-flaws` | Tests OAuth 2.0 and OpenID Connect implementations for security flaws including authorization code interception,   redirect URI manipulation |

## IAM / ZERO TRUST (54 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `analyzing-office365-audit-logs-for-compromise` |  |
| `auditing-kubernetes-cluster-rbac` | Auditing Kubernetes cluster RBAC configurations to identify overly permissive roles, wildcard permissions, dangerous   ClusterRoleBindings,  |
| `building-identity-governance-lifecycle-process` | Builds comprehensive identity governance and lifecycle management processes including joiner-mover-leaver automation,   role mining, access  |
| `building-role-mining-for-rbac-optimization` |  |
| `configuring-ldap-security-hardening` |  |
| `configuring-multi-factor-authentication-with-duo` |  |
| `configuring-oauth2-authorization-flow` |  |
| `configuring-zscaler-private-access-for-ztna` | Configuring Zscaler Private Access (ZPA) to replace traditional VPN with zero trust network access by deploying   App Connectors, defining a |
| `deploying-palo-alto-prisma-access-zero-trust` | Deploying Palo Alto Networks Prisma Access for SASE-based zero trust network access using GlobalProtect agents,   ZTNA Connectors, security  |
| `deploying-software-defined-perimeter` |  |
| `deploying-tailscale-for-zero-trust-vpn` |  |
| `exploiting-constrained-delegation-abuse` |  |
| `exploiting-kerberoasting-with-impacket` |  |
| `exploiting-nopac-cve-2021-42278-42287` |  |
| `exploiting-oauth-misconfiguration` |  |
| `exploiting-zerologon-vulnerability-cve-2020-1472` |  |
| `implementing-beyondcorp-zero-trust-access-model` | Implementing Google |
| `implementing-browser-isolation-for-zero-trust` | Deploys remote browser isolation (RBI) as a core component of a Zero Trust architecture. Implements isolation   policies with URL categoriza |
| `implementing-cisa-zero-trust-maturity-model` |  |
| `implementing-conduit-security-for-ot-remote-access` | Implement secure conduit architecture for OT remote access following IEC 62443 zones and conduits model, deploying   jump servers, MFA-enabl |
| `implementing-container-network-policies-with-calico` |  |
| `implementing-delinea-secret-server-for-pam` | Implements Delinea Secret Server for privileged access management (PAM) including secret vault configuration,   role-based access policies,  |
| `implementing-device-posture-assessment-in-zero-trust` | Implementing device posture assessment as a zero trust access control by integrating endpoint health signals   from CrowdStrike ZTA, Microso |
| `implementing-google-workspace-admin-security` | Implements comprehensive Google Workspace security hardening including admin console configuration, phishing-resistant   MFA enforcement, DL |
| `implementing-google-workspace-sso-configuration` |  |
| `implementing-identity-governance-with-sailpoint` |  |
| `implementing-identity-verification-for-zero-trust` |  |
| `implementing-just-in-time-access-provisioning` |  |
| `implementing-kubernetes-network-policy-with-calico` |  |
| `implementing-microsegmentation-with-guardicore` | Implementing microsegmentation using Akamai Guardicore Segmentation to map application dependencies, create   granular network policies, vis |
| `implementing-mtls-for-zero-trust-services` | Configures mutual TLS (mTLS) authentication between microservices using Python cryptography library for certificate   generation and ssl mod |
| `implementing-network-policies-for-kubernetes` |  |
| `implementing-pam-for-database-access` |  |
| `implementing-passwordless-authentication-with-fido2` |  |
| `implementing-privileged-access-management-with-cyberark` |  |
| `implementing-privileged-access-workstation` |  |
| `implementing-privileged-session-monitoring` | Implements privileged session monitoring and recording using Privileged Access Management (PAM) solutions, focusing   on CyberArk Privileged |
| `implementing-rbac-hardening-for-kubernetes` |  |
| `implementing-saml-sso-with-okta` |  |
| `implementing-secrets-management-with-vault` | This skill covers deploying HashiCorp Vault for centralized secrets management across cloud environments, including   dynamic secret generat |
| `implementing-zero-standing-privilege-with-cyberark` |  |
| `implementing-zero-trust-dns-with-nextdns` |  |
| `implementing-zero-trust-for-saas-applications` | Implementing zero trust access controls for SaaS applications using CASB, SSPM, conditional access policies,   OAuth app governance, and ses |
| `implementing-zero-trust-network-access` | Implementing Zero Trust Network Access (ZTNA) in cloud environments by configuring identity-aware proxies, micro-segmentation,   continuous  |
| `implementing-zero-trust-network-access-with-zscaler` |  |
| `implementing-zero-trust-with-beyondcorp` |  |
| `implementing-zero-trust-with-hashicorp-boundary` |  |
| `performing-access-review-and-certification` |  |
| `performing-kerberoasting-attack` |  |
| `performing-oauth-scope-minimization-review` | Performs OAuth 2.0 scope minimization review to identify over-permissioned third-party application integrations,   excessive API scopes, unu |
| `performing-privileged-account-access-review` |  |
| `performing-privileged-account-discovery` |  |
| `performing-service-account-audit` |  |
| `performing-service-account-credential-rotation` |  |

## PENETRATION TESTING (59 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `building-c2-infrastructure-with-sliver-framework` |  |
| `building-red-team-c2-infrastructure-with-havoc` |  |
| `bypassing-authentication-with-forced-browsing` |  |
| `executing-phishing-simulation-campaign` | Executes authorized phishing simulation campaigns to assess an organization |
| `executing-red-team-engagement-planning` |  |
| `exploiting-broken-link-hijacking` |  |
| `exploiting-deeplink-vulnerabilities` | Tests and exploits deep link (URL scheme and App Link) vulnerabilities in Android and iOS mobile applications   to identify unauthorized acc |
| `exploiting-excessive-data-exposure-in-api` | Tests APIs for excessive data exposure where endpoints return more data than the client application needs, relying   on the frontend to filt |
| `exploiting-http-request-smuggling` |  |
| `exploiting-idor-vulnerabilities` |  |
| `exploiting-insecure-data-storage-in-mobile` | Identifies and exploits insecure local data storage vulnerabilities in Android and iOS mobile applications including   unencrypted databases |
| `exploiting-insecure-deserialization` |  |
| `exploiting-jwt-algorithm-confusion-attack` | Exploits JWT algorithm confusion vulnerabilities where the server |
| `exploiting-mass-assignment-in-rest-apis` |  |
| `exploiting-ms17-010-eternalblue-vulnerability` |  |
| `exploiting-prototype-pollution-in-javascript` |  |
| `exploiting-race-condition-vulnerabilities` |  |
| `exploiting-server-side-request-forgery` |  |
| `exploiting-type-juggling-vulnerabilities` |  |
| `exploiting-vulnerabilities-with-metasploit-framework` |  |
| `exploiting-websocket-vulnerabilities` |  |
| `implementing-anti-phishing-training-program` |  |
| `implementing-dmarc-dkim-spf-email-security` |  |
| `intercepting-mobile-traffic-with-burpsuite` | Intercepts and analyzes HTTP/HTTPS traffic from mobile applications using Burp Suite proxy to identify insecure   API communications, authen |
| `performing-binary-exploitation-analysis` | Analyze binary exploitation techniques including buffer overflows and ROP chains using pwntools Python library.   Covers checksec analysis,  |
| `performing-blind-ssrf-exploitation` |  |
| `performing-clickjacking-attack-test` |  |
| `performing-credential-access-with-lazagne` |  |
| `performing-csrf-attack-simulation` |  |
| `performing-graphql-depth-limit-attack` |  |
| `performing-graphql-security-assessment` |  |
| `performing-hash-cracking-with-hashcat` |  |
| `performing-initial-access-with-evilginx3` |  |
| `performing-jwt-none-algorithm-attack` |  |
| `performing-kubernetes-penetration-testing` |  |
| `performing-lateral-movement-with-wmiexec` |  |
| `performing-mobile-app-certificate-pinning-bypass` | Bypasses SSL/TLS certificate pinning implementations in Android and iOS applications to enable traffic interception   during authorized secu |
| `performing-phishing-simulation-with-gophish` |  |
| `performing-physical-intrusion-assessment` |  |
| `performing-privilege-escalation-assessment` | Performs privilege escalation assessments on compromised Linux and Windows systems to identify paths from low-privilege   access to root or  |
| `performing-privilege-escalation-on-linux` |  |
| `performing-purple-team-exercise` | Performs purple team exercises by coordinating red team adversary emulation with blue team detection validation   using MITRE ATT&CK-mapped  |
| `performing-red-team-phishing-with-gophish` |  |
| `performing-red-team-with-covenant` |  |
| `performing-security-headers-audit` |  |
| `performing-soap-web-service-security-testing` |  |
| `performing-soc2-type2-audit-preparation` | Automates SOC 2 Type II audit preparation including gap assessment against AICPA Trust Services Criteria (CC1-CC9),   evidence collection fr |
| `performing-ssrf-vulnerability-exploitation` |  |
| `performing-threat-emulation-with-atomic-red-team` | Executes Atomic Red Team tests for MITRE ATT&CK technique validation using the atomic-operator Python framework.   Loads test definitions fr |
| `performing-web-cache-poisoning-attack` |  |
| `testing-android-intents-for-vulnerabilities` | Tests Android inter-process communication (IPC) through intents for vulnerabilities including intent injection,   unauthorized component acc |
| `testing-api-security-with-owasp-top-10` |  |
| `testing-cors-misconfiguration` |  |
| `testing-for-broken-access-control` |  |
| `testing-for-business-logic-vulnerabilities` |  |
| `testing-for-sensitive-data-exposure` |  |
| `testing-for-xss-vulnerabilities-with-burpsuite` |  |
| `testing-jwt-token-security` |  |
| `testing-mobile-api-authentication` | Tests authentication and authorization mechanisms in mobile application APIs to identify broken authentication,   insecure token management, |

## WEB & API SECURITY (24 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `implementing-api-gateway-security-controls` | Implements security controls at the API gateway layer including authentication enforcement, rate limiting, request   validation, IP allowlis |
| `implementing-api-key-security-controls` | Implements secure API key generation, storage, rotation, and revocation controls to protect API authentication   credentials from leakage, b |
| `implementing-api-rate-limiting-and-throttling` | Implements API rate limiting and throttling controls using token bucket, sliding window, and fixed window algorithms   to protect against br |
| `implementing-api-schema-validation-security` |  |
| `implementing-api-security-posture-management` |  |
| `implementing-api-security-testing-with-42crunch` |  |
| `implementing-jwt-signing-and-verification` |  |
| `implementing-web-application-logging-with-modsecurity` | Configure ModSecurity WAF with OWASP Core Rule Set (CRS) for web application logging, tune rules to reduce false   positives, analyze audit  |
| `integrating-dast-with-owasp-zap-in-pipeline` | This skill covers integrating OWASP ZAP (Zed Attack Proxy) for Dynamic Application Security Testing in CI/CD   pipelines. It addresses confi |
| `performing-api-fuzzing-with-restler` | Uses Microsoft RESTler to perform stateful REST API fuzzing by automatically generating and executing test sequences   that exercise API end |
| `performing-api-inventory-and-discovery` | Performs API inventory and discovery to identify all API endpoints in an organization |
| `performing-api-rate-limiting-bypass` | Tests API rate limiting implementations for bypass vulnerabilities by manipulating request headers, IP addresses,   HTTP methods, API versio |
| `performing-api-security-testing-with-postman` | Uses Postman to perform structured API security testing by building collections that test for OWASP API Security   Top 10 vulnerabilities in |
| `performing-content-security-policy-bypass` |  |
| `performing-threat-modeling-with-owasp-threat-dragon` |  |
| `performing-web-application-penetration-test` | Performs systematic security testing of web applications following the OWASP Web Security Testing Guide (WSTG)   methodology to identify vul |
| `performing-web-application-scanning-with-nikto` |  |
| `performing-web-application-vulnerability-triage` |  |
| `testing-api-authentication-weaknesses` | Tests API authentication mechanisms for weaknesses including broken token validation, missing authentication   on endpoints, weak password p |
| `testing-api-for-broken-object-level-authorization` | Tests REST and GraphQL APIs for Broken Object Level Authorization (BOLA/IDOR) vulnerabilities where an authenticated   user can access or mo |
| `testing-api-for-mass-assignment-vulnerability` | Tests APIs for mass assignment (auto-binding) vulnerabilities where clients can modify object properties they   should not have access to by |
| `testing-for-json-web-token-vulnerabilities` |  |
| `testing-for-xss-vulnerabilities` | Tests web applications for Cross-Site Scripting (XSS) vulnerabilities by injecting JavaScript payloads into   reflected, stored, and DOM-bas |
| `testing-websocket-api-security` | Tests WebSocket API implementations for security vulnerabilities including missing authentication on WebSocket   upgrade, Cross-Site WebSock |

## CONTAINERS & K8S (22 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `analyzing-kubernetes-audit-logs` | Parses Kubernetes API server audit logs (JSON lines) to detect exec-into-pod, secret access, RBAC modifications,   privileged pod creation,  |
| `hardening-docker-daemon-configuration` |  |
| `implementing-aqua-security-for-container-scanning` |  |
| `implementing-container-image-minimal-base-with-distroless` |  |
| `implementing-devsecops-security-scanning` | Integrates Static Application Security Testing (SAST), Dynamic Application Security Testing (DAST), and Software   Composition Analysis (SCA |
| `implementing-ebpf-security-monitoring` | Implements eBPF-based security monitoring using Cilium Tetragon for real-time process execution tracking, network   connection observability |
| `implementing-kubernetes-pod-security-standards` |  |
| `implementing-opa-gatekeeper-for-policy-enforcement` |  |
| `implementing-pod-security-admission-controller` |  |
| `implementing-policy-as-code-with-open-policy-agent` | This skill covers implementing Open Policy Agent (OPA) and Gatekeeper for policy-as-code enforcement in Kubernetes   and CI/CD pipelines. It |
| `implementing-runtime-security-with-tetragon` |  |
| `performing-container-image-hardening` | This skill covers hardening container images by minimizing attack surface, removing unnecessary packages, implementing   multi-stage builds, |
| `performing-container-security-scanning-with-trivy` |  |
| `performing-docker-bench-security-assessment` |  |
| `performing-kubernetes-cis-benchmark-with-kube-bench` |  |
| `performing-kubernetes-etcd-security-assessment` |  |
| `scanning-container-images-with-grype` |  |
| `scanning-containers-with-trivy-in-cicd` | This skill covers integrating Aqua Security |
| `scanning-docker-images-with-trivy` |  |
| `securing-container-registry-images` | Securing container registry images by implementing vulnerability scanning with Trivy and Grype, enforcing image   signing with Cosign and Si |
| `securing-container-registry-with-harbor` |  |
| `securing-helm-chart-deployments` |  |

## OT / ICS / SCADA (18 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `building-soc-metrics-and-kpi-tracking` | Builds SOC performance metrics and KPI tracking dashboards measuring Mean Time to Detect (MTTD), Mean Time to   Respond (MTTR), alert qualit |
| `implementing-iec-62443-security-zones` | This skill covers designing and implementing security zones and conduits for industrial automation and control   systems (IACS) per IEC 6244 |
| `implementing-nerc-cip-compliance-controls` | This skill covers implementing North American Electric Reliability Corporation Critical Infrastructure Protection   (NERC CIP) compliance co |
| `implementing-network-segmentation-for-ot` | This skill covers implementing network segmentation in Operational Technology environments using VLANs, industrial   firewalls, data diodes, |
| `implementing-ot-network-traffic-analysis-with-nozomi` | Deploy Nozomi Networks Guardian sensors for passive OT network traffic analysis to achieve comprehensive asset   visibility, real-time threa |
| `implementing-patch-management-for-ot-systems` | This skill covers implementing a structured patch management program for OT/ICS environments where traditional   IT patching approaches can  |
| `implementing-purdue-model-network-segmentation` | Implement network segmentation based on the Purdue Enterprise Reference Architecture (PERA) model to separate   industrial control system ne |
| `implementing-supply-chain-security-with-in-toto` |  |
| `monitoring-scada-modbus-traffic-anomalies` | Monitors Modbus TCP traffic on SCADA and ICS networks to detect anomalous function code usage, unauthorized   register writes, and suspiciou |
| `performing-bluetooth-security-assessment` |  |
| `performing-ics-asset-discovery-with-claroty` | Perform comprehensive ICS/OT asset discovery using Claroty xDome platform, leveraging passive monitoring, Claroty   Edge active queries, and |
| `performing-iot-security-assessment` | Performs comprehensive security assessments of IoT devices and their ecosystems by testing hardware interfaces,   firmware, network communic |
| `performing-oil-gas-cybersecurity-assessment` | This skill covers conducting cybersecurity assessments specific to oil and gas facilities including upstream   (exploration/production), mid |
| `performing-ot-vulnerability-assessment-with-claroty` | This skill covers performing vulnerability assessments in OT environments using the Claroty xDome platform for   comprehensive asset discove |
| `performing-ot-vulnerability-scanning-safely` | Perform vulnerability scanning in OT/ICS environments safely using passive monitoring, native protocol queries,   and carefully controlled a |
| `performing-power-grid-cybersecurity-assessment` | This skill covers conducting cybersecurity assessments of electric power grid infrastructure including generation   facilities, transmission |
| `performing-s7comm-protocol-security-analysis` | Perform security analysis of Siemens S7comm and S7CommPlus protocols used by SIMATIC S7 PLCs to identify vulnerabilities   including replay  |
| `performing-scada-hmi-security-assessment` | Perform security assessments of SCADA Human-Machine Interface (HMI) systems to identify vulnerabilities in web-based   HMIs, thin-client con |

## VULN MANAGEMENT (18 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `analyzing-sbom-for-supply-chain-vulnerabilities` | Parses Software Bill of Materials (SBOM) in CycloneDX and SPDX JSON formats to identify supply chain vulnerabilities   by correlating compon |
| `building-patch-tuesday-response-process` |  |
| `building-vulnerability-aging-and-sla-tracking` |  |
| `building-vulnerability-dashboard-with-defectdojo` |  |
| `building-vulnerability-exception-tracking-system` |  |
| `building-vulnerability-scanning-workflow` | Builds a structured vulnerability scanning workflow using tools like Nessus, Qualys, and OpenVAS to discover,   prioritize, and track remedi |
| `implementing-epss-score-for-vulnerability-prioritization` |  |
| `implementing-patch-management-workflow` |  |
| `implementing-vulnerability-management-with-greenbone` |  |
| `implementing-vulnerability-remediation-sla` |  |
| `implementing-vulnerability-sla-breach-alerting` |  |
| `performing-agentless-vulnerability-scanning` |  |
| `performing-authenticated-vulnerability-scan` |  |
| `performing-endpoint-vulnerability-remediation` | Performs vulnerability remediation on endpoints by prioritizing CVEs based on risk scoring, deploying patches,   applying configuration chan |
| `performing-vulnerability-scanning-with-nessus` | Performs authenticated and unauthenticated vulnerability scanning using Tenable Nessus to identify known vulnerabilities,   misconfiguration |
| `prioritizing-vulnerabilities-with-cvss-scoring` |  |
| `scanning-infrastructure-with-nessus` |  |
| `triaging-vulnerabilities-with-ssvc-framework` |  |

## ENDPOINT SECURITY (9 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `configuring-windows-defender-advanced-settings` | Configures Microsoft Defender for Endpoint (MDE) advanced protection settings including attack surface reduction   rules, controlled folder  |
| `deploying-edr-agent-with-crowdstrike` | Deploys and configures CrowdStrike Falcon EDR agents across enterprise endpoints to enable real-time threat   detection, behavioral analysis |
| `hardening-linux-endpoint-with-cis-benchmark` | Hardens Linux endpoints using CIS Benchmark recommendations for Ubuntu, RHEL, and CentOS to reduce attack surface,   enforce security baseli |
| `hardening-windows-endpoint-with-cis-benchmark` | Hardens Windows endpoints using CIS (Center for Internet Security) Benchmark recommendations to reduce attack   surface, enforce security ba |
| `implementing-anti-ransomware-group-policy` | Configures Windows Group Policy Objects (GPO) to prevent ransomware execution and limit its spread. Implements   AppLocker rules, Software R |
| `implementing-application-whitelisting-with-applocker` | Implements application whitelisting using Windows AppLocker to restrict unauthorized software execution on endpoints,   reducing attack surf |
| `implementing-disk-encryption-with-bitlocker` | Implements full disk encryption using Microsoft BitLocker on Windows endpoints to protect data at rest from   unauthorized access in case of |
| `implementing-endpoint-dlp-controls` | Implements endpoint Data Loss Prevention (DLP) controls to detect and prevent sensitive data exfiltration through   email, USB, cloud storag |
| `implementing-usb-device-control-policy` | Implements USB device control policies to restrict unauthorized removable media access on endpoints, preventing   data exfiltration and malw |

## RANSOMWARE DEFENSE (1 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `performing-ransomware-response` | Executes a structured ransomware incident response from initial detection through containment, forensic analysis,   decryption assessment, r |

## DEVSECOPS (7 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `building-devsecops-pipeline-with-gitlab-ci` |  |
| `implementing-github-advanced-security-for-code-scanning` |  |
| `implementing-image-provenance-verification-with-cosign` |  |
| `implementing-secret-scanning-with-gitleaks` | This skill covers implementing Gitleaks for detecting and preventing hardcoded secrets in git repositories.   It addresses configuring pre-c |
| `implementing-secrets-scanning-in-ci-cd` |  |
| `implementing-sigstore-for-software-signing` | Implements Sigstore-based software signing and verification using Cosign keyless signing, Rekor transparency   log verification, and Fulcio  |
| `performing-sca-dependency-scanning-with-snyk` | This skill covers implementing Software Composition Analysis (SCA) using Snyk to detect vulnerable open-source   dependencies in CI/CD pipel |

## CRYPTOGRAPHY (13 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `analyzing-tls-certificate-transparency-logs` | Queries Certificate Transparency logs via crt.sh and pycrtsh to detect phishing domains, unauthorized certificate   issuance, and shadow IT. |
| `auditing-tls-certificate-transparency-logs` | Monitors Certificate Transparency (CT) logs to detect unauthorized certificate issuance, discover subdomains   via CT data, and alert on sus |
| `configuring-certificate-authority-with-openssl` |  |
| `configuring-hsm-for-key-storage` |  |
| `implementing-aes-encryption-for-data-at-rest` |  |
| `implementing-digital-signatures-with-ed25519` |  |
| `implementing-end-to-end-encryption-for-messaging` |  |
| `implementing-hashicorp-vault-dynamic-secrets` | Implements HashiCorp Vault dynamic secrets engines for database credentials, AWS IAM keys, and PKI certificates   with automatic generation, |
| `implementing-zero-knowledge-proof-for-authentication` |  |
| `performing-cryptographic-audit-of-application` |  |
| `performing-hardware-security-module-integration` |  |
| `performing-post-quantum-cryptography-migration` | Assesses organizational readiness for post-quantum cryptography migration per NIST FIPS 203/204/205 standards.   Performs cryptographic inve |
| `performing-ssl-certificate-lifecycle-management` |  |

## COMPLIANCE (9 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `analyzing-cyber-kill-chain` | Analyzes intrusion activity against the Lockheed Martin Cyber Kill Chain framework to identify which phases   an adversary has completed, wh |
| `implementing-data-loss-prevention-with-microsoft-purview` | Implements data loss prevention policies using Microsoft Purview to protect sensitive information across Exchange   Online, SharePoint, OneD |
| `implementing-file-integrity-monitoring-with-aide` |  |
| `implementing-gdpr-data-subject-access-request` | Automates GDPR Data Subject Access Request (DSAR) workflows including identity verification, PII discovery across   databases and files usin |
| `implementing-iso-27001-information-security-management` |  |
| `implementing-pci-dss-compliance-controls` |  |
| `performing-access-recertification-with-saviynt` |  |
| `performing-nist-csf-maturity-assessment` | The NIST Cybersecurity Framework (CSF) 2.0, released in February 2024, provides a   comprehensive taxonomy for managing cybersecurity risk t |
| `performing-privacy-impact-assessment` | Automates the Privacy Impact Assessment (PIA) workflow including data flow mapping, privacy risk scoring matrices,   GDPR Article 35 DPIA an |

## MOBILE SECURITY (2 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `implementing-mobile-application-management` | Implements Mobile Application Management (MAM) policies to protect enterprise data on managed and unmanaged   mobile devices through app-lev |
| `performing-ios-app-security-assessment` | Performs comprehensive iOS application security assessments using Frida for dynamic instrumentation, Objection   for runtime exploration, SS |

## PHISHING & EMAIL (2 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `implementing-proofpoint-email-security-gateway` |  |
| `performing-dmarc-policy-enforcement-rollout` |  |

## OTROS (30 skills)

| Skill ID | Descripcion |
|----------|-------------|
| `analyzing-api-gateway-access-logs` | Parses API Gateway access logs (AWS API Gateway, Kong, Nginx) to detect BOLA/IDOR attacks, rate limit bypass,   credential scanning, and inj |
| `analyzing-ethereum-smart-contract-vulnerabilities` |  |
| `analyzing-powershell-script-block-logging` |  |
| `analyzing-web-server-logs-for-intrusion` |  |
| `building-soc-escalation-matrix` |  |
| `implementing-attack-path-analysis-with-xm-cyber` |  |
| `implementing-attack-surface-management` | Implements external attack surface management (EASM) using Shodan, Censys, and ProjectDiscovery tools (subfinder,   httpx, nuclei) for asset |
| `implementing-continuous-security-validation-with-bas` |  |
| `implementing-fuzz-testing-in-cicd-with-aflplusplus` |  |
| `implementing-hardware-security-key-authentication` | Implements FIDO2/WebAuthn hardware security key authentication including registration ceremonies, authentication   flows, YubiKey enrollment |
| `implementing-llm-guardrails-for-security` | Implements input and output validation guardrails for LLM-powered applications to prevent prompt injection,   data leakage, toxic content ge |
| `implementing-log-integrity-with-blockchain` |  |
| `implementing-mitre-attack-coverage-mapping` |  |
| `implementing-network-traffic-analysis-with-arkime` |  |
| `implementing-passwordless-auth-with-microsoft-entra` | Implements passwordless authentication using Microsoft Entra ID with FIDO2 security keys, Windows Hello for   Business, Microsoft Authentica |
| `implementing-rapid7-insightvm-for-scanning` |  |
| `implementing-scim-provisioning-with-okta` |  |
| `implementing-security-chaos-engineering` | Implements security chaos engineering experiments that deliberately disable or degrade security controls to   verify detection and response  |
| `implementing-syslog-centralization-with-rsyslog` |  |
| `implementing-threat-modeling-with-mitre-attack` | Implements threat modeling using the MITRE ATT&CK framework to map adversary TTPs against organizational assets,   assess detection coverage |
| `implementing-ticketing-system-for-incidents` | Implements an integrated incident ticketing system connecting SIEM alerts to ServiceNow, Jira, or TheHive for   structured incident tracking |
| `investigating-insider-threat-indicators` | Investigates insider threat indicators including data exfiltration attempts, unauthorized access patterns, policy   violations, and pre-depa |
| `performing-asset-criticality-scoring-for-vulns` |  |
| `performing-entitlement-review-with-sailpoint-iiq` | Performs entitlement review and access certification campaigns using SailPoint IdentityIQ including manager   certifications, targeted entit |
| `performing-fuzzing-with-aflplusplus` | Perform coverage-guided fuzzing of compiled binaries using AFL++ (American Fuzzy Lop Plus Plus) to discover   memory corruption, crashes, an |
| `performing-http-parameter-pollution-attack` |  |
| `performing-purple-team-atomic-testing` | Executes Atomic Red Team tests mapped to MITRE ATT&CK techniques, performs coverage gap analysis across the   ATT&CK matrix, and runs detect |
| `performing-thick-client-application-penetration-test` |  |
| `performing-web-cache-deception-attack` |  |
| `triaging-security-incident` | Performs initial triage of security incidents to determine severity, scope, and required response actions using   the NIST SP 800-61r3 and S |

---
**Directorio completo:** `skills/community-cybersec/skills/`
