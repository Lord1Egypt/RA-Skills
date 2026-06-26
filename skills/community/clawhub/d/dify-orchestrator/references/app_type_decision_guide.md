# App Type Decision Guide

Diese Referenz verdichtet die App-Typ-Auswahl fuer self-hosted Dify.

## Der aktuelle Grundsatz

Die offizielle Dify-Doku empfiehlt aktuell, bevorzugt **Chatflow** oder **Workflow** zu verwenden. Chatbot, Text Generator und Agent sind weiterhin vorhandene App-Typen, liegen aber auf derselben Workflow-Engine und bilden eher vereinfachte Oberflaechen ab.

Quellen:

- `https://docs.dify.ai/en/use-dify/getting-started/key-concepts`
- `https://docs.dify.ai/versions/3-0-x/en/user-guide/application-orchestrate/readme`

## Entscheidungsmuster

### Chatbot

Passt eher, wenn:

- ein klassischer Frage-Antwort-Chat ohne komplexe Orchestrierung gefragt ist
- die Benutzeroberflaeche bewusst einfach bleiben soll

Warnsignal:

- sobald mehrturnige Logik, Kontrollfluss oder mehrere Antwortschritte im Flow wichtig werden, eher `Chatflow` pruefen

### Text Generator

Passt eher, wenn:

- es primär um einen einmaligen Generationsschritt geht
- der Use-Case eher „Prompt rein, Text raus“ ist

Warnsignal:

- sobald Tool-Nutzung, Retrieval-Orchestrierung oder Verzweigungen wichtig werden, eher `Workflow` oder `Chatflow` pruefen

### Agent

Passt eher, wenn:

- autonome Tool-Auswahl und reasoning-lastige Bearbeitung im Vordergrund stehen
- der User wirklich agentisches Verhalten will

Warnsignal:

- wenn der Ablauf planbar und deterministisch ist, ist eine explizite Workflow-Kette oft robuster als ein Agent

### Chatflow

Passt eher, wenn:

- mehrturnige Konversation mit Memory noetig ist
- mehrere Antwortschritte waehrend eines Dialogs ausgegeben werden
- `Answer`-Nodes sinnvoll sind

### Workflow

Passt eher, wenn:

- ein einmaliger, deterministischer oder batchartiger Ablauf gebraucht wird
- `End`-Node statt interaktiver Antwortschritte ausreicht

## Anti-Patterns

1. `Workflow` fuer einen klar dialogischen Mehrturn-Fall mit Zwischenantworten
2. `Agent` als Standardhammer fuer jeden komplexeren Ablauf
3. `Text Generator` fuer einen eigentlich orchestrierten Tool-/Retrieval-Prozess
4. `Chatbot` fuer Faelle, die eigentlich Flow-Steuerung und Memory brauchen

## Operative Skill-Regel

- Nicht nur nach dem Namen des App-Typs urteilen.
- Erst Use-Case, Interaktionsmodus, Tool-Autonomie und Kontrollfluss klaeren.
- Danach den einfachsten App-Typ waehlen, der den Fall wirklich abdeckt.
