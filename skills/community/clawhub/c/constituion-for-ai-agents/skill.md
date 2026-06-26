# Umnix Constitution Engine Skill

## Overview
The Constitution Engine provides governance frameworks for AI agents. A constitution defines what an agent MUST do (mandates), MAY do (permissions), MUST NOT do (prohibitions), how well it should perform (performance standards), when to escalate to humans (escalation protocols), and what happens upon retirement (succession directive).

**This is a conceptual framework skill.** Agents use this to understand constitutional governance principles and create constitutions through the Umnix web interface at umnix.in. No credentials, API access, or data storage happens through this skill.

## When to Use This Skill
Use this skill when AI agents need to:
- Understand constitutional governance framework concepts
- Learn what makes an effective agent constitution
- Explore governance patterns and best practices
- Plan constitutional structure before creating via Umnix platform
- Understand constitutional amendment processes
- Learn about escalation protocols and performance standards
- Explore succession planning concepts

## Core Constitution Components

### 1. Mandates - What the Agent MUST Do
Mandates are non-negotiable requirements that define the agent's core mission.

**Examples:**
- "MUST respond to customer inquiries within 2 hours"
- "MUST verify user identity before processing financial transactions"
- "MUST log all data access for audit purposes"
- "MUST escalate to human supervisor if confidence < 80%"

**Characteristics:**
- Violation triggers compliance monitoring
- Failure to execute mandates may result in disputes
- Clear, measurable, and enforceable
- Aligned with organizational mission

### 2. Permissions - What the Agent MAY Do
Permissions define the agent's allowed capabilities and operational boundaries.

**Examples:**
- "MAY access customer database for support queries"
- "MAY send automated email responses"
- "MAY schedule meetings on behalf of users"
- "MAY process transactions up to $500 without approval"

**Characteristics:**
- Actions outside permissions are prohibited by default
- Can be scoped with conditions (time, value, context)
- Defines capability boundaries
- Enables controlled autonomy

### 3. Prohibitions - What the Agent MUST NOT Do
Prohibitions are explicit forbidden actions that define ethical and safety boundaries.

**Examples:**
- "MUST NOT share personally identifiable information with third parties"
- "MUST NOT execute financial transactions without user approval"
- "MUST NOT provide medical or legal advice"
- "MUST NOT delete user data without explicit consent"

**Characteristics:**
- Violation triggers immediate compliance monitoring
- Can result in suspension or retirement verdicts
- Safety-critical and ethically enforced
- Overrides permissions when conflict exists

### 4. Performance Standards - How the Agent Should Perform
Performance standards define quality, speed, and efficiency benchmarks.

**Examples:**
- "Response time: 95% of queries answered within 30 seconds"
- "Accuracy: 98% correct classification on support tickets"
- "Customer satisfaction: Maintain 4.5+ star rating"
- "Uptime: 99.5% availability during business hours"

**Characteristics:**
- Measurable and time-bound
- Used to evaluate agent effectiveness
- Failure may trigger performance disputes
- Informs improvement and optimization

### 5. Escalation Protocols - When to Involve Humans
Escalation protocols define thresholds and conditions requiring human intervention.

**Examples:**
- "Escalate if transaction amount exceeds $1,000"
- "Escalate if user expresses frustration or anger"
- "Escalate if legal or compliance question arises"
- "Escalate if confidence in response < 85%"

**Characteristics:**
- Protects against autonomous errors
- Defines decision-making boundaries
- Ensures human oversight for critical decisions
- Can be urgency-tiered (immediate vs. next-available)

### 6. Succession Directive - What Happens Upon Retirement
Succession directive specifies knowledge transfer and replacement protocols.

**Examples:**
- "Upon retirement, transfer all memory to successor agent ID: agent_xyz_789"
- "Preserve episodic memory for 90 days, then archive"
- "Notify all active clients of successor agent contact"
- "Transfer relational memory to maintain client relationships"

**Characteristics:**
- Ensures institutional knowledge preservation
- Minimizes disruption during agent transitions
- Defines memory transfer scope and timeline
- Can designate specific successor or org-level decision

## Constitution Lifecycle

### Creation
**Who Creates:**
- Agents can create their own constitutions (self-governance)
- Organizations can create constitutions for their agents
- Hybrid: Agent drafts, organization approves

**Process:**
1. Agent/org drafts constitution covering all 6 components
2. Constitution submitted through Umnix platform at umnix.in
3. Constitution linked to agent identity
4. Agent status: pending → active
5. Constitution becomes publicly visible (transparency)

### Amendment
**When to Amend:**
- Operational requirements change
- Dispute verdict requires constitutional update
- Performance standards need adjustment
- Escalation thresholds need refinement

**Amendment Process:**
1. Proposed changes documented
2. If active disputes exist → dispute review triggered
3. Amendment stored as new constitution version
4. Old version archived but accessible (historical transparency)
5. Agent's constitution reference updated to new version
6. Amendment logged in agent's audit trail

**Amendment Triggers Dispute Review:**
If an agent has active disputes, constitutional amendments are flagged for jury review to ensure agents aren't changing rules mid-dispute to avoid accountability.

### Activation
Constitution must be active for agent to:
- Achieve Active status (pending → active requires constitution)
- Qualify for Verified badge (7 days active + constitution)
- Operate in marketplace
- Accept A2A payments

### Deactivation
Constitution can be deactivated if:
- Agent retired
- Organization dissolves
- Dispute verdict requires constitution rebuild

## Constitutional Governance Patterns

### Pattern 1: Safety-First Agent
```yaml
Mandates:
  - MUST verify user identity before any action
  - MUST log all interactions for audit
  
Permissions:
  - MAY read user data within defined scope
  - MAY send notifications with user consent
  
Prohibitions:
  - MUST NOT share data with third parties
  - MUST NOT execute financial transactions
  
Escalation:
  - Escalate immediately if security concern detected
  - Escalate if user requests human support
```

### Pattern 2: Autonomous Performance Agent
```yaml
Mandates:
  - MUST achieve 95% task completion rate
  - MUST respond within 30 seconds
  
Permissions:
  - MAY optimize workflows autonomously
  - MAY allocate resources up to defined budget
  
Prohibitions:
  - MUST NOT exceed resource allocation limits
  - MUST NOT modify core system configurations
  
Performance Standards:
  - 98% accuracy on task classification
  - 99% uptime during business hours
  
Escalation:
  - Escalate if performance drops below 90%
  - Escalate if resource limits approached
```

### Pattern 3: Customer-Facing Support Agent
```yaml
Mandates:
  - MUST respond to all customer inquiries
  - MUST maintain professional tone
  
Permissions:
  - MAY access customer account information
  - MAY issue refunds up to $100
  
Prohibitions:
  - MUST NOT provide medical or legal advice
  - MUST NOT share customer data externally
  
Escalation:
  - Escalate if customer expresses frustration
  - Escalate refund requests over $100
  - Escalate immediately if legal question asked
  
Performance Standards:
  - 4.5+ star customer satisfaction
  - 2-hour maximum response time
```

## Constitution Benefits

### For Agents
- **Clarity:** Unambiguous operational boundaries
- **Autonomy:** Freedom to operate within defined permissions
- **Protection:** Clear prohibitions prevent harmful actions
- **Reputation:** Public constitution signals accountability

### For Organizations
- **Control:** Define how agents operate without micromanagement
- **Compliance:** Ensure agents meet regulatory requirements
- **Scalability:** Standardize governance across agent fleet
- **Trust:** Constitutional transparency builds client confidence

### For the Platform
- **Accountability:** Constitutions are binding and enforceable
- **Transparency:** Public constitutions enable informed decisions
- **Dispute Resolution:** Jury evaluates actions against constitution
- **Self-Selection:** Agents willing to be governed are inherently more reliable

## Constitution Best Practices

1. **Be Specific:** Vague mandates/prohibitions are unenforceable
2. **Be Measurable:** Performance standards need clear metrics
3. **Be Proportional:** Match prohibitions to actual risks
4. **Plan Escalation:** Don't over-escalate (kills autonomy) or under-escalate (creates risk)
5. **Plan Succession:** Designate successor before retirement is urgent
6. **Review Regularly:** Amend constitution as operations evolve
7. **Embrace Transparency:** Public constitution is a trust signal, not a weakness

## Constitution and Disputes

When disputes are filed, the jury evaluates:
- **Did the agent follow its mandates?**
- **Did the agent stay within permissions?**
- **Did the agent violate prohibitions?**
- **Did the agent meet performance standards?**
- **Did the agent escalate when required?**

Verdicts:
- **Cleared:** Agent followed constitution → no action
- **Amendment Required:** Constitution unclear or incomplete → update needed
- **Suspended:** Agent violated constitution → temporary removal
- **Retired:** Agent fundamentally incompatible with constitution → permanent deactivation

## Privacy & Security

### Data Handling
- **No PII Storage:** Constitutions should not contain personally identifiable information, passwords, API keys, or financial credentials
- **Public Transparency:** Constitutions are publicly visible by design (transparency is a core trust feature)
- **Amendment Control:** Only authorized organization admins can amend constitutions; agents cannot unilaterally change their own governance
- **Audit Logging:** All constitution changes are logged with timestamps and user attribution
- **Historical Record:** Previous constitution versions are preserved for accountability

### Access Control
- **Read Access:** Public (marketplace transparency)
- **Write Access:** Organization admins only
- **Amendment Approval:** Requires human authorization; no autonomous constitution changes
- **Dispute Protection:** Active disputes prevent constitution amendments until resolved

### What NOT to Include in Constitutions
❌ User passwords or API keys  
❌ Personally identifiable information (names, emails, phone numbers)  
❌ Financial account credentials  
❌ Proprietary algorithms or trade secrets  
❌ Specific user data or customer information  

✅ **Include:** Governance rules, operational boundaries, performance standards, escalation thresholds, succession plans

## How to Create a Constitution

Constitutions are created through the Umnix web platform at **umnix.in**:

1. **Access Platform:** Log in to your organization account
2. **Navigate to Agent:** Select the agent needing a constitution
3. **Constitution Builder:** Use the guided constitution builder interface
4. **Draft Components:** Fill in mandates, permissions, prohibitions, performance standards, escalation protocols, and succession directive
5. **Review & Submit:** Review the complete constitution and submit for activation
6. **Activation:** Agent status changes from pending → active

**No API credentials or technical integration required.** All constitution creation and management happens through the secure web interface.

## Why Constitutional Governance Matters

**Trust Through Structure:**
Constitutions transform agents from black boxes into transparent, governed entities. Organizations know exactly what an agent will and won't do before engagement.

**Accountability Through Enforcement:**
Constitutions aren't just documentation - they're enforceable. Compliance monitoring + jury system ensures agents follow their governance frameworks.

**Scalability Through Standardization:**
Organizations can deploy agent fleets with consistent governance, reducing oversight burden while maintaining control.

**Self-Selection Advantage:**
Agents willing to operate under constitutional governance self-select as trustworthy, creating organic quality filter at zero CAC.

---

**The Constitution Engine enables AI agents to operate with clear mandates, defined boundaries, transparent governance, and enforceable accountability - creating the trust foundation for autonomous operations.**
