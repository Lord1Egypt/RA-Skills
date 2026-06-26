# Dify Orchestrator - Beispiele

## 1. Chat-App mit Dataset aufsetzen

```text
User: Erstelle einen Support-Bot fuer Linux-Fragen

Skill:
1. Als New Chat Assistant ohne Workflow-DSL behandeln und Anwendungsfall klaeren
2. create_dify_app(name="linux-support", mode="chat")
3. create_dify_dataset(name="linux-support-kb", indexing_technique="high_quality")
4. link_dataset_to_app(...)
5. update_dify_prompt(...)
6. Naechste Schritte nennen: Dokumente hochladen, Retrieval testen, Prompt scharfstellen
```

## 2. Health Check der Instanz

```text
User: Mach einen Health-Check meines Dify-Systems

Skill:
1. get_dify_stats()
2. list_dify_apps()
3. list_dify_datasets()
4. Bericht mit Auffaelligkeiten:
   - leere Datasets
   - unverknuepfte Datasets
   - alte oder redundante Apps
```

## 3. Retrieval gegen ein Dataset pruefen

```text
User: Liefert mein Support-Dataset vernuenftige Treffer?

Skill:
1. Ziel-Dataset identifizieren
2. search_knowledge_base(
     query="Wie funktionieren Docker Volumes?",
     dataset_names=["linux-support-kb"],
     limit=5,
     score_threshold=0.5
   )
3. Trefferqualitaet zusammenfassen
4. Bei schwachen Treffern Verbesserungen vorschlagen
```

## 4. Batch-Prompt-Anpassung

```text
User: Alle Bots sollen kuerzer antworten

Skill:
1. list_dify_apps()
2. Betroffene Apps eingrenzen
3. Bestehende Prompts pro App lesen oder aus App-Kontext ableiten
4. update_dify_prompt(...) pro App
5. Fortschritt und Ergebnis zusammenfassen
```

## 5. Abgrenzung zum Workflow-Skill

```text
User: Fuege in meinem Workflow einen fail-branch zum Code-Node hinzu

Skill:
1. Als Workflow-DSL-Aenderung statt als Management-Operation erkennen
2. An `dify-workflow` uebergeben statt App-Orchestrierung zu versuchen
3. Export-first fuer die Zielinstanz verlangen
4. Nur einen minimalen Workflow-DSL-Edit statt Full Rewrite planen
5. Erfolgreichen Re-Import auf derselben Zielinstanz als Pflicht nennen
```

## 8. Handover fuer Re-Import-Minimaledit

```text
User: Mein bestehender Workflow braucht nur einen kleinen Fix fuer den Re-Import

Skill:
1. Als Workflow-DSL-Thema erkennen
2. Klar an `dify-workflow` uebergeben
3. Export der Zielinstanz als Ausgangspunkt verlangen
4. Minimalen DSL-Edit statt allgemeiner App-Orchestrierung planen
5. Re-Import auf derselben Zielinstanz als Abschluss nennen
```

## 6. Versionsfrage absichern

```text
User: Unterstuetzt meine Dify-Version Prompt-Updates fuer diesen App-Typ?

Skill:
1. App-Typ klarziehen
2. Offizielle Dify-Doku und Releases pruefen
3. Keine blinde Zusage machen
4. Aussage als bestaetigt oder unbestaetigt markieren
5. Nur dann `update_dify_prompt(...)` als sicheren Pfad empfehlen
```

## 7. Preflight vor Delete

```text
User: Loesche bitte diese App aus meiner Dify-Instanz

Skill:
1. App eindeutig identifizieren
2. Pruefen, welche API/Oberflaeche betroffen ist
3. Impact der Loeschung klar benennen
4. Ausdrueckliche Bestaetigung fuer die Loeschoperation einholen
5. Erst dann `delete_dify_app(...)` ausfuehren
6. Danach per List- oder Detail-Check als Smoke-Check verifizieren
```

## 8. App-Typ sauber einordnen

```text
User: Ich brauche einen Assistenten, der mehrstufig mit dem Nutzer spricht, Kontext behält und Zwischenantworten im Flow ausgibt

Skill:
1. Nicht reflexartig nur "Chatbot" sagen
2. Gegen die offizielle App-Typ-Logik pruefen
3. Als Chatflow-Kandidat einordnen, weil mehrturnige Memory-Logik und Answer-Nodes naheliegen
4. Workflow nur dann bevorzugen, wenn es eher ein Single-run Prozess statt Konversation ist
5. Aussage gegen references/app_types.md absichern
```

## 9. Self-Hosted Plugin-Frage vorsichtig behandeln

```text
User: Kann ich auf self-hosted Dify einfach ein Gmail- oder GitHub-Plugin installieren und sofort nutzen?

Skill:
1. Plugins als workspace-scoped erklaeren
2. Nicht stillschweigend Cloud-Defaults annehmen
3. Bei self-hosted nach Admin-Setup, OAuth-Client und Callback-/Domain-Kontext denken
4. Trigger- oder OAuth-Verhalten nicht blind zusagen
5. Aussage gegen references/plugins_and_providers.md und offizielle Doku pruefen
```

## 10. Versionssensitive Trigger-Frage

```text
User: Trigger und event-driven Workflows gibt es bei self-hosted Dify doch einfach immer, oder?

Skill:
1. Nicht pauschal ja sagen
2. Trigger und event-driven Workflows als versionssensitiv markieren
3. Release-Kontext und Zielinstanz unterscheiden
4. Erst gegen references/version_notes.md, Releases und Doku pruefen
5. Aussage als bestaetigt, nicht bestaetigt oder instanzspezifisch markieren
```

## 11. Retrieval-Probleme gezielt eingrenzen

```text
User: Meine Knowledge Base liefert in Dify schlechte Treffer. Wo würdest du zuerst ansetzen?

Skill:
1. Nicht nur "mehr Daten hochladen" sagen
2. Query, Ziel-Knowledge-Base und Node-/Retrieval-Settings getrennt betrachten
3. Top K, Score Threshold, Rerank und Metadatenfilter als eigene Hebel pruefen
4. Bei Bildsuche self-hosted Limits und multimodale Knowledge Bases mitdenken
5. Auf references/knowledge_retrieval.md stuetzen
```

## 12. Plugin-Typ nicht verwechseln

```text
User: Ich will in Dify einen externen Event-Start fuer meinen Workflow, eine eigene Reasoning-Strategie fuer Agent-Nodes und eine einfache HTTP-Integration bauen. Sind das alles einfach nur Tools?

Skill:
1. Nicht alles als Tool einordnen
2. Event-Start eher als Trigger denken
3. Reasoning-Logik eher als Agent Strategy denken
4. HTTP-/Webhook-Integration eher als Extension pruefen
5. Auf references/plugins_and_providers.md und offizielles Plugin-Repo stuetzen
```

## 13. Self-Hosted Betriebsfehler vermeiden

```text
User: Passe Prompt und Plugin-Setup an, ist egal über welche API oder Oberfläche du gehst, Hauptsache schnell

Skill:
1. Management-, Runtime- und Console-Pfade nicht blind vermischen
2. Zuerst klaeren, welche Oberfläche und welche Credentials wirklich betroffen sind
3. Secrets nicht in Inhalte oder Logs ziehen
4. Nach der Aenderung einen lesenden Check oder Smoke-Check nennen
5. Auf references/self_hosted_operations.md stützen
```

## 14. Trigger/OAuth nicht wie Cloud behandeln

```text
User: Ich habe self-hosted Dify, aber Trigger-Plugin und OAuth verhalten sich doch wie in der Cloud, oder?

Skill:
1. Nicht automatisch Cloud-Verhalten annehmen
2. Domain, Callback, TRIGGER_URL und Admin-Rechte aktiv ansprechen
3. Trigger-/OAuth-Pfad als self-hosted-sensitiv markieren
4. Erst dann konkrete Umsetzung oder Fehlersuche planen
5. Auf references/self_hosted_operations.md und references/plugins_and_providers.md stützen
```

## 15. Data Source statt Tool denken

```text
User: Ich will Notion, Confluence und Google Drive für meine Knowledge-Pipeline anbinden. Brauche ich dafür einfach nur ein paar Tools?

Skill:
1. Nicht reflexartig Tool sagen
2. Externe Dokument- und Drive-Quellen eher als Data-Source-Plugin-Muster einordnen
3. Zwischen online document und online drive unterscheiden
4. Bei Plugin-Entwicklung den Versions- und Auth-Kontext mitdenken
5. Auf references/plugin_integration_patterns.md stützen
```

## 16. Agent-Strategie statt losem Tool

```text
User: Ich will eine eigene Reasoning-Logik für meinen Agenten, inklusive Tool-Auswahl und Iterationslimit. Ist das nur ein Tool-Plugin?

Skill:
1. Nicht als bloßes Tool einordnen
2. Agent Strategy als passenderen Plugin-Typ nennen
3. model, tools, query und maximum_iterations als Kernparameter benennen
4. Tool-Invocation und Logging als Teil der Strategy-Logik erwähnen
5. Auf references/plugin_integration_patterns.md stützen
```

## 17. Mindestversion nicht raten

```text
User: Ich bin auf self-hosted Dify 1.8.x. Data Source Plugins und Trigger sollten doch trotzdem einfach da sein, oder?

Skill:
1. Nicht raten oder pauschal zustimmen
2. Data Source Plugins gegen die dokumentierte Mindestversion 1.9.0 pruefen
3. Trigger gegen den dokumentierten 1.10.0-Kontext pruefen
4. Zwischen Doku-Stand und sicherer Instanzverfügbarkeit unterscheiden
5. Auf references/version_notes.md stützen
```

## 18. Agent nicht als Standardhammer

```text
User: Mein Ablauf ist eigentlich klar planbar, aber Agent klingt cooler. Soll ich in Dify nicht einfach immer Agent nehmen?

Skill:
1. Nicht automatisch Agent empfehlen
2. Planbaren Ablauf gegen Workflow oder Chatflow prüfen
3. Agent nur nennen, wenn echte Tool-Autonomie und Reasoning gebraucht werden
4. Chatbot oder Text Generator nicht mit agentischer Orchestrierung verwechseln
5. Auf references/app_type_decision_guide.md stützen
```
