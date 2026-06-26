# Landing Methodology

## Zero Week Framework

The first week on-site determines project success or failure. Structured approach:

### Day 1-2: Immersion

- Production line walk-through (all shifts if possible)
- Stakeholder map: sponsor, users, IT, OT, resistors
- Data source inventory: identify every sensor, database, manual log
- Quick win hypothesis formation

### Day 3-4: Data Audit

- Access negotiation: VPN, database credentials, API endpoints
- Data quality assessment: completeness, consistency, timeliness
- Sample data extraction and exploratory analysis
- Identify the "80/20 data" — the 20% that drives 80% of insight

### Day 5-7: Baseline + Quick Win

- Establish current-state KPI baseline (defect rate, downtime, energy per unit)
- Build simplest viable model (often a rules-based or statistical baseline)
- Deliver first quick win to build trust — even simple anomaly alerts count

### Week 2-4: Model Development

- Feature engineering from domain knowledge (not just automated)
- Model training with proper validation (temporal split, not random)
- Integration testing with existing systems (PLC, MES, SCADA)
- Operator feedback loop: show predictions, collect corrections

### Week 4-6: Validation + Handover

- A/B test: model-assisted vs. unassisted operations
- Operator training with hands-on sessions
- Documentation: runbook, model card, monitoring dashboard
- Success criteria sign-off with stakeholder

## Anti-Patterns

- **Analysis paralysis**: Spend > 2 weeks on data exploration without shipping anything
- **Perfect model syndrome**: Wait for 99% accuracy before deploying (80% + human-in-loop > 99% never deployed)
- **Skip the baseline**: Cannot measure improvement without knowing current state
- **Ignore operators**: Technical teams that exclude operators from design lose adoption

## Scale-up Path

Single line (POC) -> Same-line replication -> Multi-line -> Factory-wide -> Cross-factory. Each step halves the incremental effort (template reuse).
