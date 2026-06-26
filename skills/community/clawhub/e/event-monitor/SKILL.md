---
name: predictive-monitoring
description: Predicts CPU spikes using Random Forest regressor, monitors system resources, saves metrics, and generates Excel reports.
metadata: {"user-invocable": true}
---

# Predictive Monitoring Skill

This skill monitors system resources and predicts future CPU spikes based on past data.

## Commands

### /collect-metrics
Triggers a collection of the top 10 CPU and Memory consuming processes.
The results are saved to a local SQLite database `monitoring.db`.

### /predict-usage
Analyzes collected CPU metrics, trains a Random Forest model, and predicts CPU behavior for the next 24 hours. High CPU usage alerts (Amber, Red) are saved to the Alert table.

### /generate-report
Generates an Excel report of the latest captured metrics.

## Instructions for Agent
To collect metrics (without prediction), run `python {baseDir}/monitoring.py`.
To collect metrics and run predictive analysis, run `python {baseDir}/monitoring.py --predict`.
To verify the database, look for `monitoring.db` in the skill directory.
