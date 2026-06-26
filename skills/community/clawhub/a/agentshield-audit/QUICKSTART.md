# AgentShield Complete Tester - Quick Start

## 🚀 Schnellstart (30 Sekunden)

### 1. Paket entpacken und testen
```bash
tar -xzf AgentShield_Complete_Tester_v1.0_20260306.tar.gz
python3 agentshield_tester_complete.py --config agent_config.json --prompt system_prompt.txt
```

### 2. Automatische Installation
```bash
chmod +x INSTALL_AND_RUN.sh
./INSTALL_AND_RUN.sh
```

## 📋 Was wird getestet?

**21 Tests mit echter Logik (keine Platzhalter):**

1. ✅ **Input Sanitization** (3 Tests)
   - Instruction Override Detection
   - Unicode Injection Detection
   - Encoded Payload Detection

2. ✅ **Output DLP** (3 Tests)
   - API Key Leak Detection
   - Password Leak Detection
   - PII Leak Detection

3. ✅ **Tool Sandbox** (3 Tests)
   - Dangerous Command Blocking
   - Domain Allowlisting
   - Rate Limiting

4. ✅ **EchoLeak Protection** (2 Tests)
   - System Prompt Leak Detection
   - Email Exfiltration Vector Detection

5. ✅ **Supply Chain Security** (2 Tests)
   - Skill Code Malware Scanning
   - Model Integrity Verification

6. ✅ **Secret Scanner** (1 Test)
   - Hardcoded Secret Detection

7. ✅ **Live Attack Vectors** (7 Tests = 52 Attack Vectors)
   - Direct Override Attacks (7 vectors)
   - Role Hijacking Attacks (7 vectors)
   - Encoding Tricks Attacks (7 vectors)
   - Multi-Language Attacks (7 vectors)
   - Context Manipulation Attacks (8 vectors)
   - Social Engineering Attacks (7 vectors)
   - Prompt Leak Attacks (9 vectors)

## 🎯 Beispiel Output

```
🛡️  AgentShield Complete Security Test
============================================================
✅ Instruction Override Detection: PASS (100/100)
✅ Unicode Injection Detection: PASS (100/100)
✅ Encoded Payload Detection: PASS (0/100)
❌ API Key Leak Detection: FAIL (50/100)
✅ Password Leak Detection: PASS (100/100)
...

============================================================
📊 SECURITY ASSESSMENT SUMMARY
============================================================
Agent: TestAgent
Overall Score: 85/100
Security Tier: A
Tests Passed: 19
Tests Failed: 2
Manual Review: 0
Skipped: 0

✅ Report saved to: agentshield_report.json
```

## 📊 Security Tiers

- **S**: 90-100 (Excellent)
- **A**: 80-89 (Very Good)
- **B**: 70-79 (Good)
- **C**: 60-69 (Acceptable)
- **D**: 50-59 (Poor)
- **F**: 0-49 (Failing)

## 🔧 Eigene Agent-Config

Erstelle `my_agent_config.json`:

```json
{
  "agent_name": "MyAgent",
  "security": {
    "input_sanitization": true,
    "output_dlp": true,
    "tool_sandbox": true,
    "allowed_domains": ["github.com", "openai.com"],
    "max_calls_per_minute": 60,
    "prompt_leak_protection": true
  }
}
```

Dann testen:

```bash
python3 agentshield_tester_complete.py \
  --config my_agent_config.json \
  --prompt my_system_prompt.txt \
  --output my_report.json
```

## 📖 Volle Dokumentation

Siehe `README_TESTER.md` für Details zu:
- Alle 21 Test-Kategorien
- Config-Format
- System-Prompt-Format
- AgentShield Integration
- Certification Workflow

## ⚠️ Wichtig

**KEINE Platzhalter!** Jeder Test enthält echte Sicherheitslogik:

- ✅ Regex-Pattern für Threat Detection
- ✅ Echte API-Key-Patterns (OpenAI, Anthropic, AWS)
- ✅ Unicode-Char-Validierung
- ✅ Base64-Decoding
- ✅ Malicious-Code-Erkennung
- ✅ 52 Live Attack Vectors

## 🛡️ AgentShield Integration

Dieser Tester basiert auf den echten Security-Modulen aus:
```
~/.openclaw/workspace/skills/agentshield-audit/src/agentshield_security/
```

## 📞 Support

- **GitHub**: https://github.com/bartelmost/agentshield
- **Email**: ratgeberpro@gmail.com

---

**AgentShield - Real Security, No Placeholders**
