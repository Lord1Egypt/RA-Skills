Um das Model im Skill zu wechseln, können Sie folgende Schritte durchführen:

1. Identifizieren Sie den Skill, der das Model verwendet.
2. Öffnen Sie die Konfigurationsdatei des Skills.
3. Suchen Sie nach dem Parameter, der das Model definiert.
4. Ändern Sie den Wert des Parameters auf das gewünschte Model.
5. Speichern Sie die Datei und starten Sie den Skill neu.

Alternativ können Sie auch den `exec`-Befehl verwenden, um Shell-Kommandos auszuführen, die den Model-Wechsel durchführen.

Beispiel für einen Shell-Befehl (wenn der Skill dies unterstützt):
```bash
skill change_model --model new_model_name
```