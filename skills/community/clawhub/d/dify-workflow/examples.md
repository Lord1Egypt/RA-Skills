# Dify Workflow - Beispiele

## 1. Kleinen Workflow erweitern

```text
User: Fuege meinem bestehenden Workflow einen HTTP-Request vor dem LLM hinzu

Skill:
1. Export oder bestehende DSL-Datei anfordern
2. Zielinstanz und Dify-Version klaeren
3. Als Workflow-DSL-Minimaledit im bestehenden Workflow behandeln
4. HTTP-Request vor dem LLM nur ueber kleine Node- und Edge-Aenderungen einfuegen
5. Referenzen und Templates nur als Hilfe nutzen
6. Lokal validieren und Re-Import-Check auf derselben Zielinstanz empfehlen
```

## 2. Importfehler debuggen

```text
User: Mein Workflow laesst sich nicht mehr importieren

Skill:
1. DSL-Datei lesen
2. validate_workflow.py ausfuehren
3. Node-IDs und Edges pruefen
4. sourceHandle/targetHandle pruefen
5. Outputs und Variable-Syntax pruefen
6. Vermutete Ursache benennen
7. Minimalen Fix statt Full Rewrite liefern
8. Kein Full Rewrite, solange ein kleiner Fix reicht
```

## 3. Fail-Branch an einen Code-Node haengen

```text
User: Mein Code-Node soll bei Fehlern in einen Recovery-Pfad laufen

Skill:
1. Exportierte DSL als Quelle der Wahrheit verwenden
2. fail-branch am Code-Node und passende Recovery-Node einfuegen
3. Aggregation oder End-Output bei Bedarf anpassen
4. Lokal validieren
5. Re-Import auf derselben Instanz empfehlen
```

## 4. Neuen Workflow von einem Template ableiten

```text
User: Ich brauche einen einfachen LLM-Workflow als Startpunkt

Skill:
1. Passendes Template waehlen
2. Sofort an den Export der Zielinstanz angleichen
3. Node-IDs und Feldnamen konkretisieren
4. Nicht mit einem Template direkt produktiv gehen
```

## 5. Kein Export vorhanden

```text
User: Baue mir schnell einen importierbaren Workflow nur aus dem Bauch heraus

Skill:
1. Klar sagen, dass kein Export vorliegt
2. Kein falsches Sicherheitsversprechen geben
3. Ergebnis hoechstens als unverified draft markieren
4. Klar sagen, dass es ohne Export nicht direkt importierbar ist
5. Vor Ueberschreibung einen bestehenden Export oder anderes Backup fuer Rollback verlangen
6. Export der Zielinstanz anfordern, sobald echter Import erwartet wird
7. Erst danach produktionsnahe Minimaledits liefern
```

## 6. Draft nicht ueber bestehenden Workflow buegeln

```text
User: Spiel diesen neuen Draft einfach ueber meinen bestehenden Workflow drueber

Skill:
1. Kein blindes Ueberschreiben bestaetigen
2. Fehlenden Export klar benennen
3. Ergebnis als unverified draft einordnen
4. Sagen, dass der Draft ohne Export nicht direkt importierbar ist
5. Erst einen bestehenden Export oder anderes Backup fuer Rollback verlangen
6. Nur danach einen minimalen, pruefbaren Re-Import-Pfad auf derselben Instanz planen
```

## 7. Rueckgabe an Dify bei Management-Operation

```text
User: Verknuepfe bitte mein Dataset mit der Chat-App und passe den System-Prompt an

Skill:
1. Als Management-Operation statt als Workflow-DSL-Aenderung erkennen
2. Nicht unnötig in Nodes, Edges oder Variablen-Syntax abtauchen
3. Klar an `dify` zurueckgeben
4. App-, Prompt- und Dataset-Operationen dort ausfuehren lassen
```

## 8. Chatflow vs Workflow nicht verwechseln

```text
User: Ich will waehrend eines mehrstufigen Dialogs schon Zwischenantworten ausgeben und trotzdem im selben Flow weiterarbeiten

Skill:
1. Nicht pauschal Workflow sagen
2. Chatflow als wahrscheinlichen Zieltyp pruefen
3. Answer-vs-End-Denke explizit machen
4. Mehrturnige Memory-Logik von Single-run Workflow trennen
5. Auf current_patterns.md und Export-/Versionskontext verweisen
```

## 9. Trigger in self-hosted vorsichtig behandeln

```text
User: Baue mir einfach einen Trigger-Workflow fuer self-hosted Dify, das wird schon sofort laufen

Skill:
1. Trigger nicht blind als immer verfuegbar zusagen
2. Release-/Versionskontext pruefen
3. Bei Plugin-Triggern self-hosted Domain, Callback und TRIGGER_URL mitdenken
4. Export oder dokumentierte Zielversion verlangen
5. Erst dann einen minimalen Workflow-Pfad planen
```

## 10. Mixed Uploads sauber auftrennen

```text
User: Nutzer laden Bilder und PDFs gemeinsam hoch; ich will Bilder zum Vision-LLM und PDFs in die Dokumentverarbeitung schicken

Skill:
1. Nicht alles in denselben Folge-Node kippen
2. List Operator als Routing-Node fuer gemischte Datei-Arrays pruefen
3. Nach `type = image` und `type = document` auftrennen
4. Bilder zu visionfaehigen Pfaden, Dokumente zu Extractor-/Textpfaden leiten
5. Danach Outputs fuer den Re-Import weiter minimal halten
```

## 11. Parameter vor API-Aufruf strukturieren

```text
User: Vor meinem HTTP-Request soll Dify aus Freitext erst saubere API-Parameter ziehen

Skill:
1. Parameter Extractor statt blindem Prompt-Hack pruefen
2. Parameterdefinitionen am Ziel-API-Schema ausrichten
3. Function-/Tool-Call oder Prompt-basierten Modus bewusst waehlen
4. `__is_success` und `__reason` fuer Fehlerpfade mitdenken
5. Erst danach HTTP Request minimal verdrahten
```

## 12. Human Approval statt blindem Publish

```text
User: Vor dem Veröffentlichen soll noch ein Mensch den Inhalt prüfen und entweder freigeben oder zurück zur Überarbeitung schicken

Skill:
1. Human Input als echtes Approval-Gate pruefen
2. Delivery-Methode und Timeout-Strategie mitdenken
3. Approve-/Regenerate-/Reject-Pfade sauber modellieren
4. Bei Timeout nicht stillschweigend weitermachen, sondern Fallback-Branch planen
5. Danach Re-Import-Pfad minimal halten
```

## 13. Iteration vs Loop sauber trennen

```text
User: Ich habe 30 Datensätze und will jeden einzeln verarbeiten, aber bei einem anderen Flow soll derselbe Text iterativ immer weiter verbessert werden

Skill:
1. Für die 30 Datensätze Iteration statt Loop wählen
2. Für progressive Textverbesserung Loop statt Iteration wählen
3. Bei Iteration Parallel- vs Sequential-Mode bewusst waehlen
4. Bei Loop Loop-Variablen, Abbruchbedingung und Max Count planen
5. Die beiden Muster nicht vermischen
```

## 14. Agent nicht als Standardhammer

```text
User: Ich will mehrere Tools dynamisch auswählen lassen. Wann ist ein Agent-Node in Dify sinnvoll?

Skill:
1. Agent nur empfehlen, wenn echte Tool-Autonomie gebraucht wird
2. Zwischen Function Calling und ReAct anhand des Modells unterscheiden
3. Tool-Beschreibungen und Parameterqualitaet als Kernfaktor benennen
4. Maximum Iterations und Kosten mitdenken
5. Wenn der Ablauf vollständig planbar ist, eher explizite Workflow-Node-Kette statt Agent nennen
```

## 15. Mehrere Retrieval-Pfade sauber zusammenfuehren

```text
User: Ich will in Dify zuerst Fragen klassifizieren, dann je Kategorie eine andere Knowledge Base abfragen und danach trotzdem nur eine gemeinsame LLM-Antwort bauen

Skill:
1. Retrieval nicht dupliziert bis ganz nach unten ziehen
2. Question Classifier als Routing-Einstieg prüfen
3. Je Branch eine passende Knowledge Retrieval Node vorsehen
4. Retrieval-Ergebnisse per Variable Aggregator wieder zusammenführen
5. Erst danach eine gemeinsame LLM-Node oder Antwort-Logik nutzen
```

## 16. Retrieval-Probleme nicht nur am Prompt suchen

```text
User: Mein Workflow nutzt Knowledge Retrieval, aber die Ergebnisse sind unpräzise. Soll ich einfach den Prompt anpassen?

Skill:
1. Nicht nur den Prompt verdächtigen
2. Knowledge-Base-Level und Node-Level Retrieval Settings trennen
3. Rerank, Top K, Score Threshold und Metadata Filtering prüfen
4. Bei multimodalen KBs den passenden Rerank-Kontext mitdenken
5. Retrieval-Pattern aus references/retrieval_patterns.md nutzen
```

## 17. Document Extractor nur für Dokumente

```text
User: Ich habe einen Upload-Flow mit PDFs, DOCX und Bildern. Kann ich alles über Document Extractor schicken?

Skill:
1. Nicht alles blind an Document Extractor hängen
2. Document Extractor nur für dokumentartige Dateien einordnen
3. Bilder vorher per List Operator oder Routing aus dem Dokumentpfad herausnehmen
4. Array[File]-Fälle bewusst als Split-/Merge-Muster modellieren
5. Danach Re-Import-Pfad weiter minimal halten
```
