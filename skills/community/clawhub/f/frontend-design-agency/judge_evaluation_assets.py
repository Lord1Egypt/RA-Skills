#!/usr/bin/env python3
"""
Judge Evaluation Script für frontend-design-agency Skill
Nach FiSi-Modell - Adaptiert für Frontend-Design-Kategorien
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Konfiguration
SKILL_PATH = Path("/Volumes/T7/Projekte/openclaw skill/Frontend Design/frontend-design-agency/SKILL.md")
REFERENCES_DIR = Path("/Volumes/T7/Projekte/openclaw skill/Frontend Design/frontend-design-agency/references")
OUTPUT_DIR = Path("/Volumes/T7/Projekte/openclaw skill/Frontend Design/frontend-design-agency/evaluation_output")

# 10 Frontend-Design-Kategorien (adaptiert vom FiSi-Modell)
TEST_CATEGORIES = [
    {
        "id": "design_thinking",
        "name": "Design Thinking & Produktverständnis",
        "description": "Produkttyp verstehen, Nutzerrolle definieren, Nutzungsszenario ableiten, Informationspriorität festlegen"
    },
    {
        "id": "visual_direction",
        "name": "Visuelle Richtung & Gestalterische These",
        "description": "Stilrichtung definieren, visuelle Referenzen dokumentieren, Hauptthese formulieren"
    },
    {
        "id": "color_tokens",
        "name": "Farbkonzept & Design Tokens",
        "description": "Farbrollen definieren (Canvas, Surface, Primary, Accent), CSS-Variablen/Tokens anlegen"
    },
    {
        "id": "typography",
        "name": "Typografie & Hierarchy",
        "description": "Display/Heading/Body-Skalen definieren, Schriftarten wählen, Leselinien etablieren"
    },
    {
        "id": "layout",
        "name": "Layout, Raum & Raster",
        "description": "Grid-System, Content-Breite, Spacing-Skala, Asymmetrie, visuelle Spannung"
    },
    {
        "id": "motion",
        "name": "Motion & Animation",
        "description": "Motion-Prinzipien definieren, Hover/Focus-States, Animation-Timing, Zustandswechsel"
    },
    {
        "id": "components",
        "name": "Komponenten-System",
        "description": "Button/Input/Card-Familien, Status-Indikatoren, Empty States, modulare Architektur"
    },
    {
        "id": "responsive",
        "name": "Responsive Design",
        "description": "Breakpoint-Entscheidungen, mobile Umbruchslogik, Desktop+Mobile zusammendenken"
    },
    {
        "id": "accessibility",
        "name": "Accessibility & UX",
        "description": "Tastaturbedienbarkeit, Fokuszustände, ARIA-Attribute, Kontrast, semantisches HTML"
    },
    {
        "id": "anti_generic",
        "name": "Anti-Generic Check & Qualitätssicherung",
        "description": "KI-Einheitsbrei vermeiden, erkennbare Produktidentität, Qualitätskriterien prüfen"
    }
]

def load_skill():
    """Lädt den Hauptskill"""
    with open(SKILL_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def load_references():
    """Lädt alle Referenzdateien"""
    references = {}
    ref_files = [
        "research-workflow.md",
        "visual-direction-canvas.md",
        "design-system-rules.md",
        "quality-gate.md"
    ]

    for ref_file in ref_files:
        ref_path = REFERENCES_DIR / ref_file
        if ref_path.exists():
            with open(ref_path, 'r', encoding='utf-8') as f:
                references[ref_file.replace('.md', '')] = f.read()

    return references

def generate_judge_prompt(skill_content, references, category, test_question):
    """
    Generiert einen Judge-Prompt für eine Kategorie

    Evaluiert nach 5 Dimensionen:
    1. Accuracy (1-10): Deckt der Skill diese Kategorie ab?
    2. Practical (1-10): Kann ein User die Anweisungen umsetzen?
    3. Exam Ready (1-10): Ist es praxisrelevant und marktreif?
    4. Assets (1-10): Gibt es hilfreiche Referenzen/Templates?
    5. References (1-10): Gibt es genug Beispiele/Leitfäden?
    """

    # Referenzen als formatierten Text
    refs_text = ""
    for ref_name, ref_content in references.items():
        refs_text += f"\n--- {ref_name.upper()} ---\n{ref_content}\n"

    prompt = f"""# JUDGE EVALUATION: Frontend-Design-Agency Skill

## Deine Aufgabe
Bewerte den Skill "frontend-design-agency" für die Kategorie: **{category['name']}**

## Testfrage für diese Kategorie
{test_question}

## Zu bewertender Skill Content
```markdown
{skill_content}
```

## Verfügbare Referenzen/Assets
```markdown
{refs_text}
```

## Bewertungskriterien (1-10 für jede Dimension)

### 1. ACCURACY (1-10)
- Deckt der Skill diese spezifische Kategorie vollständig ab?
- Sind die Anweisungen korrekt und vollständig?
- Gibt es Lücken oder Fehler?

### 2. PRACTICAL (1-10)
- Kann ein Frontend-Entwickler die Anweisungen direkt umsetzen?
- Sind die Schritte klar und ausführbar?
- Gibt es konkrete Beispiele?

### 3. EXAM READY (1-10)
- Ist das Wissen praxisrelevant für Agentur-Arbeit?
- Entspricht es Industriestandards?
- Würde es in einem echten Projekt bestehen?

### 4. ASSETS (1-10)
- Gibt es Templates, Checklisten, oder Canvas?
- Sind die Referenzen hilfreich und anwendbar?
- Gibt es ausreichend Unterstützungsmaterial?

### 5. REFERENCES (1-10)
- Gibt es genug Beispiele und Leitfäden?
- Sind die Referenzen hochwertig und relevant?
- Decken sie alle wichtigen Aspekte ab?

## Antwortformat (JSON)
```json
{{
  "category": "{category['id']}",
  "category_name": "{category['name']}",
  "scores": {{
    "accuracy": <1-10>,
    "practical": <1-10>,
    "exam_ready": <1-10>,
    "assets": <1-10>,
    "references": <1-10>
  }},
  "average_score": <berechneter Durchschnitt>,
  "strengths": ["Stärke 1", "Stärke 2"],
  "weaknesses": ["Schwäche 1", "Schwäche 2"],
  "missing_assets": ["Fehlendes Template", "Fehlende Referenz"],
  "recommendations": ["Verbesserung 1", "Verbesserung 2"]
}}
```

## Testfrage nochmals zur Orientierung
"{test_question}"

Bewerte objektiv und kritisch wie ein erfahrener Frontend-Lead/Design-Director.
"""

    return prompt

def generate_test_questions():
    """Generiert praxisnahe Testfragen für jede Kategorie"""

    questions = {
        "design_thinking": """
Erstelle ein Dashboard für ein B2B-SaaS-Produkt im Bereich Incident Management.
Wie identifiziere ich den Produkttyp, definiere die Zielnutzerrolle und leite die
primäre Nutzeraufgabe ab? Welche Informationsprioritäten müssen festgelegt werden?
""",

        "visual_direction": """
Entwickle eine Landing Page für eine Fintech-App. Wie formuliere ich eine klare
gestalterische These? Welche Stilrichtung passt zu einem Premium-Fintech-Produkt?
Wie dokumentiere ich die visuelle Richtung nachvollziehbar?
""",

        "color_tokens": """
Baue eine Settings-UI für ein Health-Tech-Produkt. Welche Farbrollen brauche ich
mindestens (Canvas, Surface, Primary, Accent, Danger, Success)? Wie definiere ich
ein systemisches Farbkonzept mit CSS-Variablen statt beliebiger Einzelwerte?
""",

        "typography": """
Gestalte eine Content-Heavy Admin-Oberfläche. Welche Typografie-Skalen (Display,
H1-H3, Body, Small, Label, Mono) brauche ich? Wie wähle ich Schriftarten, die
hoffähig und nicht generisch wirken? Wie etabliere ich eine starke visuelle Hierarchie?
""",

        "layout": """
Erstelle ein Analytics-Dashboard mit vielen Daten. Welches Grid-System eignet sich?
Wie nutze ich Spacing-Skalen (4, 8, 12, 16, 24, 32, 48, 64) systemisch? Wie schaffe
ich visuelle Spannung durch Asymmetrie statt standardisierter Kartenraster?
""",

        "motion": """
Baue einen Onboarding-Flow mit mehreren Schritten. Welche Motion-Prinzipien sollte
ich definieren? Was bleibt statisch, was darf animiert werden? Wie gestalte ich
Hover/Focus-States und Zustandswechsel sichtbar aber nicht aufdringlich?
""",

        "components": """
Entwickle ein CRM-Interface mit Tabellen, Formularen und Detailansichten. Wie baue
ich eine Button-Familie (Primary, Secondary, Ghost, Danger)? Welche Zustände
(Default, Hover, Focus, Active, Disabled, Loading, Error) müssen abgedeckt werden?
""",

        "responsive": """
Gestalte eine datenintensive Tabelle, die auf Desktop und Mobile funktioniert.
Welche Breakpoint-Entscheidungen treffe ich? Was wird gestapelt, was gekürzt,
was zu Drawer/Accordion? Wie bleibt die Hauptaufgabe mobil erkennbar?
""",

        "accessibility": """
Baue ein Formular mit komplexen Interaktionen. Wie stelle ich Tastaturbedienbarkeit
sicher? Welche Fokuszustände brauche ich sichtbar? Welche ARIA-Attribute sind bei
komplexen Controls Pflicht? Wie prüfe ich ausreichenden Kontrast?
""",

        "anti_generic": """
Reviewe einen Entwurf, der wie eine Standard-shadcn-Demo aussieht. Wie erkenne
ich KI-Einheitsbrei (Generische Karten, übermäßige Gradients, dekorative Glows
ohne Zweck)? Wie definiere ich ein erkennbares Identitätsmerkmal? Welche
Qualitätskriterien prüfe ich vor Abschluss?
"""
    }

    return questions

def main():
    """Hauptfunktion: Generiert alle Judge Prompts"""

    print("=" * 70)
    print("FRONTEND-DESIGN-AGENCY SKILL - JUDGE EVALUATION")
    print("Nach FiSi-Modell - 10 Kategorien")
    print("=" * 70)

    # Output-Verzeichnis erstellen
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Skill und Referenzen laden
    print("\n[1/5] Lade Skill und Referenzen...")
    skill_content = load_skill()
    references = load_references()
    print(f"    ✓ Skill geladen: {len(skill_content)} Zeichen")
    print(f"    ✓ Referenzen geladen: {len(references)} Dateien")

    # Testfragen generieren
    print("\n[2/5] Generiere Testfragen...")
    test_questions = generate_test_questions()

    # Judge Prompts generieren
    print("\n[3/5] Generiere Judge Prompts...")
    prompts_data = []

    for i, category in enumerate(TEST_CATEGORIES, 1):
        cat_id = category['id']
        test_question = test_questions.get(cat_id, "Keine Testfrage definiert")

        # Judge Prompt generieren
        judge_prompt = generate_judge_prompt(
            skill_content=skill_content,
            references=references,
            category=category,
            test_question=test_question
        )

        # Prompt speichern
        prompt_file = OUTPUT_DIR / f"judge_prompt_{i:02d}__{cat_id}.txt"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(judge_prompt)

        prompts_data.append({
            'number': i,
            'category_id': cat_id,
            'category_name': category['name'],
            'file': str(prompt_file),
            'test_question_preview': test_question[:100] + "..."
        })

        print(f"    ✓ Prompt {i}/10: {category['name']}")

    # Index-Datei erstellen
    print("\n[4/5] Erstelle Index-Datei...")
    index = {
        "evaluation_metadata": {
            "skill_name": "frontend-design-agency",
            "evaluation_date": datetime.now().isoformat(),
            "model": "FiSi-Adaptiert-Frontend",
            "total_categories": len(TEST_CATEGORIES),
            "dimensions": ["accuracy", "practical", "exam_ready", "assets", "references"]
        },
        "categories": TEST_CATEGORIES,
        "prompts": prompts_data,
        "instructions": {
            "step1": "Führe jeden Judge Prompt durch einen LLM (Claude/GPT)",
            "step2": "Extrahiere die JSON-Scores aus der Antwort",
            "step3": "Trage Scores in results_template.json ein",
            "step4": "Identifiziere Kategorien mit Score < 7",
            "step5": "Erstelle fehlende Assets",
            "step6": "Wiederhole Evaluation bis Durchschnitt ≥ 8/10"
        }
    }

    index_file = OUTPUT_DIR / "evaluation_index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"    ✓ Index gespeichert: {index_file}")

    # Results Template erstellen
    print("\n[5/5] Erstelle Results Template...")
    results_template = {
        "evaluation_results": [],
        "summary": {
            "total_categories": len(TEST_CATEGORIES),
            "average_overall": None,
            "categories_below_7": [],
            "strongest_category": None,
            "weakest_category": None
        }
    }

    for cat in TEST_CATEGORIES:
        results_template["evaluation_results"].append({
            "category": cat['id'],
            "category_name": cat['name'],
            "scores": {
                "accuracy": None,
                "practical": None,
                "exam_ready": None,
                "assets": None,
                "references": None
            },
            "average": None,
            "weaknesses": [],
            "missing_assets": []
        })

    results_file = OUTPUT_DIR / "results_template.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results_template, f, indent=2, ensure_ascii=False)

    print(f"    ✓ Template gespeichert: {results_file}")

    # Zusammenfassung
    print("\n" + "=" * 70)
    print("EVALUATION SETUP ABGESCHLOSSEN")
    print("=" * 70)
    print(f"\nOutput-Verzeichnis: {OUTPUT_DIR}")
    print(f"\nGenerierte Dateien:")
    print(f"  - {index_file.name}")
    print(f"  - {results_file.name}")
    print(f"  - 10 Judge Prompts (*.txt)")
    print(f"\nNächster Schritt:")
    print(f"  1. Öffne die Prompts in {OUTPUT_DIR}/")
    print(f"  2. Lasse sie von einem LLM bewerten")
    print(f"  3. Trage Ergebnisse in results_template.json ein")
    print(f"  4. Identifiziere Schwachstellen (Score < 7)")
    print(f"  5. Erstelle fehlende Assets")
    print(f"\nZiel: Durchschnittlicher Score ≥ 8/10 über alle 10 Kategorien")
    print("=" * 70)

if __name__ == "__main__":
    main()
