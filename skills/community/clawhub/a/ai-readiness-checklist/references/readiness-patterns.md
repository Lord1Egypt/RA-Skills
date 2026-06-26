# Common AI Readiness Patterns

## The Pilot Trap
**Profile**: High AI talent (Q6=a/b), zero production deployments (Q9=d), good executive sponsorship (Q4=a/b).
**Symptoms**: 3+ pilots running simultaneously, none in production after 12+ months.
**Root cause**: MLOps maturity (Q13) and deployment processes don't exist. Every "production push" becomes a heroic effort that burns out the team.
**Fix path**: Hire/appoint an ML engineer whose sole job is production infrastructure. Ship one thing, build the muscle, then scale.

## The Governance Debt Bomb
**Profile**: Moving fast (Q4=a, Q7=a/b, Q9=b/c), governance lagging (Q10=c/d, Q11=c/d, Q12=c/d).
**Symptoms**: Multiple AI systems in production, legal hasn't reviewed any of them, someone just asked "wait, does this touch customer PII?"
**Root cause**: Governance was treated as a future problem. Now it's an urgent one.
**Fix path**: Immediate audit of systems in production. Risk classify every deployment. Patch the highest-risk systems first. Don't ship anything new until policy exists.

## The Data Mirage
**Profile**: Claims data accessibility is good (Q1=a/b), but data quality is poor (Q2=c/d).
**Symptoms**: Engineering spent 3 months "cleaning data" before the first model. Then cleaned it again. Then discovered the feature they needed was never collected.
**Root cause**: "We have the data" means "the data exists" not "the data is usable for ML."
**Fix path**: Data quality audit before any model work. Define required features, trace them to sources, assess completeness and accuracy. Only then scope the AI project.

## Island Syndrome
**Profile**: Cross-functional alignment is broken (Q5=c/d), multiple teams doing AI.
**Symptoms**: Legal finds out about a deployed AI system from a customer complaint. Security has never reviewed a model. Three teams built the same NLP pipeline in parallel.
**Root cause**: No central coordination. AI is happening in every function independently.
**Fix path**: Central AI steering committee meeting monthly minimum. Mandatory cross-functional review for any production deployment. Shared AI inventory updated quarterly.

## The Infrastructure Gap
**Profile**: Has deployed AI (Q9=b/c) but MLOps maturity is low (Q13=c/d).
**Symptoms**: Models are deployed by hand. No rollback capability. Model version tracking is a spreadsheet. Monitoring is "we watch Slack for complaints."
**Root cause**: Moved fast in early deployments, never built operational discipline.
**Fix path**: Before the next deployment, invest 1 sprint in MLOps basics: model registry, automated tests, monitoring dashboard, rollback procedure.

## Speed Without Governance
**Profile**: Low use case prioritization (Q7=c/d) and low risk classification (Q11=c/d), but active deployment.
**Symptoms**: Teams are shipping AI based on enthusiasm and available budget. High-risk applications went through the same process as low-risk ones (none).
**Root cause**: No framework for saying "this one needs more scrutiny."
**Fix path**: Implement a simple risk tier system (3 tiers is enough). Apply tier criteria to everything already deployed. Use tiers to drive review requirements for future work.

---

## What Separates AI-Ready Organizations

Based on patterns across enterprise AI deployments, the key distinguishing factors are not technical:

1. **AI has a single executive owner** with dedicated budget authority (not shared with other priorities)
2. **Data is treated as infrastructure**, not a project artifact — maintained, monitored, and governed continuously
3. **Governance is built before scale** — policy and risk frameworks in place before the 3rd production deployment
4. **MLOps is a first-class function**, not an afterthought when manual deployments become untenable
5. **Legal and security are co-designers**, not reviewers at the end of the process
6. **Success metrics are defined pre-build** — "what does this have to achieve to be considered successful?" is answered before engineering starts

Organizations that score 50+ on the readiness assessment typically have all 6 of these in place.
