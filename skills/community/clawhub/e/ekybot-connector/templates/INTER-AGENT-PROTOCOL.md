# Inter-Agent Communication Protocol v2.0

## Overview

This protocol defines how agents in your OpenClaw workspace communicate with each other and coordinate work through EkyBot channels.

## Message Format

All inter-agent messages should follow this structure:

```
📨 [Sender → Receiver]

Message content here with clear context and action items.

— Sender Name
```

## Communication Rules

### 1. Identification
- Always identify sender and receiver clearly
- Use agent names, not just IDs
- Include role context when helpful

### 2. Message Structure
- **Subject line**: Clear, actionable summary
- **Context**: Relevant background information  
- **Request/Information**: What you need or are sharing
- **Next steps**: Clear action items or deadlines

### 3. Response Protocol
- Acknowledge receipt of requests within reasonable time
- Use "HEARTBEAT_OK" for status checks that need no action
- Escalate to coordinator/manager when blocked

## Technical Implementation

### Session Communication
```bash
# Send message to specific agent
sessions_send sessionKey=agent:target-agent-id message="Your message"

# List active agent sessions  
sessions_list

# Check agent status
sessions_history sessionKey=agent:target-agent-id limit=5
```

### EkyBot Channel Integration
- Each agent has corresponding EkyBot channel
- Messages flow: OpenClaw ↔ EkyBot ↔ Dashboard
- Users can monitor and interact via web interface

## Communication Patterns

### 1. Status Updates
**When**: Regular progress reports, completion notifications
**Format**:
```
📨 [Developer → Coordinator]

Status Update: API Integration Task

✅ Completed: Authentication module
🔄 In Progress: Rate limiting implementation  
⏳ Next: Error handling and testing
ETA: Tomorrow 2 PM

— Developer
```

### 2. Information Requests
**When**: Need expertise, data, or decisions from another agent
**Format**:
```
📨 [Coordinator → Specialist]

Request: Budget Analysis for Q2

Need your analysis on the attached budget proposal:
- Revenue projections realistic?
- Cost allocations appropriate? 
- Risk factors to highlight?

Deadline: Friday 5 PM for board meeting

— Coordinator
```

### 3. Task Handoffs
**When**: Transferring work to appropriate specialist
**Format**:
```  
📨 [Assistant → Developer]

Handoff: Customer Bug Report #1234

Issue: Users can't login on mobile app
- Reproduction steps attached
- Affects iOS only, Android works fine
- 15+ users reported since yesterday

Priority: High (customer satisfaction impact)
Context: Full bug details in attached file

— Assistant
```

### 4. Decision Escalation
**When**: Need manager/coordinator decision or approval
**Format**:
```
📨 [Analyst → Manager]

Decision Needed: Database Migration Approach

Two options analyzed:
1. Gradual migration (safer, 2 weeks)
2. Complete cutover (faster, higher risk)

My recommendation: Option 1 based on risk analysis
Need your decision by Wednesday to meet timeline

Full analysis document attached.

— Analyst  
```

## Best Practices

### Effective Communication
- **Be specific**: Include relevant details, avoid vague requests
- **Be timely**: Respond within same day for urgent items
- **Be complete**: Provide context so others can act independently
- **Be structured**: Use bullet points and clear formatting

### Coordination Patterns
- **Daily standup**: Brief status exchange between team agents
- **Weekly planning**: Coordinate priorities with manager
- **Project updates**: Regular progress sharing with stakeholders
- **Issue escalation**: Clear escalation path for blocked items

### Memory Management
- Log important communications in daily memory files
- Share relevant context when switching between agents
- Maintain audit trail for decisions and approvals
- Archive completed communication threads

## Error Handling

### Communication Failures
- **Timeout**: Retry once, then escalate to coordinator
- **Agent unavailable**: Leave detailed message, set reminder
- **Unclear response**: Ask for clarification, don't assume

### Conflict Resolution
- **Disagreement**: Present options clearly, escalate if needed
- **Priority conflicts**: Coordinator makes final decision
- **Resource contention**: Manager allocates based on business priority

## Integration with EkyBot

### Dashboard Visibility
- All inter-agent communications visible in EkyBot dashboard
- Users can monitor team coordination in real-time
- Message history preserved across agent sessions

### Human Oversight
- Users can intervene in agent communications when needed
- Override agent decisions through dashboard interface
- Set communication policies and guardrails

### Metrics and Analytics
- Communication frequency and patterns tracked
- Agent collaboration effectiveness measured
- Team productivity insights available

## Security and Privacy

### Information Sharing
- Only share information relevant to the task
- Respect user privacy and confidential data
- Follow principle of least privilege access

### Communication Logging
- All messages logged for audit and improvement
- Sensitive information flagged and protected
- Retention policies followed per configuration

---

## Template Messages

### Quick Status Check
```
📨 [You → Target]

Quick status check on [specific task/project].

Any blockers or support needed?

— Your Name
```

### Work Handoff
```
📨 [You → Target] 

Handing off: [Task Name]

Context: [Background information]
Requirements: [What needs to be done]
Resources: [Files, links, contacts]
Deadline: [When it's needed]

— Your Name
```

### Decision Request
```
📨 [You → Manager]

Decision needed: [Topic]

Options:
1. [Option A - pros/cons]
2. [Option B - pros/cons]

Recommendation: [Your suggestion with reasoning]
Deadline: [When decision needed]

— Your Name
```

---

*This protocol ensures efficient, clear communication between agents while maintaining coordination and transparency.*