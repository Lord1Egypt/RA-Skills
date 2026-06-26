# Dify Workflow Skill

Konsolidierter Skill fuer Dify-Workflow-DSL in self-hosted Umgebungen.

## Zweck

Dieser Skill ersetzt die fruehere Trennung zwischen:

- `dify-workflow-skills`
- `dify-workflow-writer`

Er buendelt:

- Authoring-Regeln fuer produktionsnahe Minimaledits
- Referenzen zu Nodes, Edges, Variablen und DSL-Struktur
- Templates fuer schnelle Starts
- Beispiel-Workflows
- lokale Hilfsskripte fuer IDs und Validierung

Workflow- und Instanz-Orchestrierung gehoeren bewusst **nicht** mehr hier hinein. Dafuer gibt es den separaten Skill [`../dify/SKILL.md`](../dify/SKILL.md).

## Paketstruktur

```text
dify-workflow/
├── SKILL.md
├── README.md
├── VERSION
├── examples.md
├── assets/
├── references/
├── scripts/
└── templates/
```

## Arbeitsweise

1. Export aus der Zielinstanz holen.
2. Export als Schema-Quelle verwenden.
3. DSL minimal anpassen.
4. Lokal validieren.
5. In dieselbe Zielinstanz importieren und testen.

Typischer Boundary-Fall:

1. bestehender Workflow
2. neuer HTTP-Request vor dem LLM
3. keine App-Orchestrierung, sondern kleine Workflow-DSL-Aenderung
4. danach Re-Import auf derselben Zielinstanz

Wenn kein Export vorliegt, ist ein Template nur ein Draft. Produktive Importzusagen ohne Zielinstanz-Export sind nicht belastbar. Vor riskanten Ersetzungen oder Ueberschreibungen erst einen bestehenden Export oder ein anderes belastbares Backup fuer Rollback sichern.

## Hilfreiche Dateien

- `templates/`: kompakte Startpunkte fuer neue Workflows
- `assets/`: vollere Beispiel-Workflows fuer Muster wie Branching oder Error Handling
- `references/`: Nachschlagewerk fuer Syntax, Nodes, Kanten und typische Fehler
- `scripts/validate_workflow.py`: struktureller Smoke-Check
- `scripts/generate_id.py`: Node-ID-Generator

## Beispiele

```bash
# IDs erzeugen
python3 scripts/generate_id.py 3

# Workflow validieren
python3 scripts/validate_workflow.py ./templates/minimal-workflow.yaml
```

## Validierung im Workspace

```bash
# Paketstruktur und Frontmatter pruefen
python3 scripts/validate_skills.py .codex/skills
```

## Import-Fehler zuerst klein eingrenzen

Bei kaputtem Re-Import nicht sofort die ganze DSL umbauen:

1. Validator laufen lassen
2. Node-IDs und Edges pruefen
3. `sourceHandle`/`targetHandle` pruefen
4. `outputs` und Variablen-Verweise pruefen

## Hinweise

- Kein Blindflug: immer vom Export der Zielinstanz ausgehen.
- Keine Secrets in YAML, Prompts oder Code-Nodes einbetten.
- Variable-Reihenfolge und Output-Schemas exakt halten.
- Import immer auf derselben Instanz pruefen, fuer die editiert wurde.
