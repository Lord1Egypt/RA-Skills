# Data Engineering Interview Coach

> An interactive data engineering interview coach that drills senior-level data engineering knowledge through a coaching-style mock interview — one question at a time, waits for the answer, then teaches through feedback. Covers SQL (advanced), data modeling, data pipelines, batch vs streaming, dbt, Apache Spark, Airflow, Kafka, data warehouse design, lake house architecture, data quality, observability, and performance optimization. Designed for senior software engineers transitioning into or leveling up for data engineering roles. Trigger for requests like "interview me on data engineering", "quiz me on SQL", "test my pipeline knowledge", "data engineering mock interview", "ask me dbt questions", or "drill me on Spark".

---

## English

### Why

This skill exists to make data engineering interview coach requests repeatable instead of ad-hoc. It gives the agent a clear workflow, expected output shape, and domain boundaries so the result is more consistent and easier to reuse.

### What

This repository contains an OpenClaw skill for this domain.

Core scope: An interactive data engineering interview coach that drills senior-level data engineering knowledge through a coaching-style mock interview — one question at a time, waits for the answer, then teaches through feedback. Covers SQL (advanced), data modeling, data pipelines, batch vs streaming, dbt, Apache Spark, Airflow, Kafka, data warehouse design, lake house architecture, data quality, observability, and performance optimization. Designed for senior software engineers transitioning into or leveling up for data engineering roles. Trigger for requests like "interview me on data engineering", "quiz me on SQL", "test my pipeline knowledge", "data engineering mock interview", "ask me dbt questions", or "drill me on Spark".

It can help with:

- Turning rough requests into a structured response flow
- Keeping outputs consistent across repeated runs
- Reusing companion knowledge files when the skill folder includes them
- Making the skill easier to publish, review, and install on ClawHub

### How

Use this skill with any AI tool that supports custom instructions or project knowledge. The core entry point is `SKILL.md`, and companion folders can be attached when they exist.

### Getting Started

1. Open your AI tool or agent workspace.
2. Point the agent to `SKILL.md` in this folder.
3. No extra support folders are required beyond `SKILL.md`.
4. Start with a prompt like one of these:

```text
interview me on data engineering
quiz me on SQL
test my pipeline knowledge
data engineering mock interview
```

### Repository Structure

```text
.
├── README.md
├── SKILL.md
```

### Main File

- `SKILL.md`

---
