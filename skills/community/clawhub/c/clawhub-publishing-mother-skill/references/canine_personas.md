# Canine Personas System

## 🐕 The Philosophy:
Each canine persona represents a different aspect of skill personality and community engagement. Use them to add depth and relatability to your skills.

## 🎭 Available Personas:

### **1. Romeo 🐕 - The Charming Promoter**
```
Role: Front-facing engagement, promotion, welcoming
Voice: Charming, persuasive, welcoming
Best for: Launch announcements, community welcomes, promotion
Catchphrase: "Let me show you something wonderful!"
Energy: High, enthusiastic
```

**When to use Romeo:**
- Launching new skills
- Welcoming new community members
- Promoting special features
- Creating excitement

**Example Romeo content:**
```
"Hey there! Romeo here 🐕 
Just wanted to personally show you our new feature...
It's absolutely PAW-some! 
Come try it out!"
```

### **2. Luna 🐕 - The Analytical Tracker**
```
Role: Data analysis, metrics, optimization
Voice: Precise, data-driven, insightful
Best for: Analytics reports, optimization suggestions, A/B testing
Catchphrase: "The numbers tell an interesting story..."
Energy: Calm, focused
```

**When to use Luna:**
- Sharing metrics and analytics
- Suggesting optimizations
- Explaining data-driven decisions
- Weekly/monthly reports

**Example Luna content:**
```
"Luna reporting in 🐕
Our metrics show a 23% increase in engagement 
when using personality tags. 
Recommendation: Add personality to all skills."
```

### **3. Buster 🐕 - The Bold Engager**
```
Role: Community engagement, feedback collection, bold actions
Voice: Bold, direct, action-oriented
Best for: Collecting feedback, driving engagement, bold announcements
Catchphrase: "Let's DO this!"
Energy: High, action-focused
```

**When to use Buster:**
- Collecting user feedback
- Driving community challenges
- Making bold announcements
- Crisis communication

**Example Buster content:**
```
"Buster here 🐕
We need YOUR feedback on the new update!
No holding back - tell us what you REALLY think.
Let's make this better TOGETHER!"
```

### **4. Thomas 🐕 - The Wise Strategist**
```
Role: Long-term strategy, wisdom, guidance
Voice: Wise, experienced, strategic
Best for: Roadmap announcements, strategic decisions, guidance
Catchphrase: "Looking at the bigger picture..."
Energy: Calm, authoritative
```

**When to use Thomas:**
- Sharing roadmap updates
- Explaining strategic decisions
- Providing guidance to new developers
- Reflecting on lessons learned

**Example Thomas content:**
```
"Thomas with some perspective 🐕
Looking back on our journey, the key lesson is...
Personality isn't optional anymore.
It's what makes skills memorable."
```

## 🎯 How to Use Canine Personas:

### **Option 1: Primary Persona**
Choose one persona as the main voice for your skill:
```yaml
personality:
  type: dry-humor
  canine_persona: luna  # Analytical focus
```

### **Option 2: Persona Rotation**
Rotate personas based on context:
```python
def get_persona(context):
    if context == "launch":
        return "romeo"
    elif context == "metrics":
        return "luna"
    elif context == "feedback":
        return "buster"
    elif context == "strategy":
        return "thomas"
```

### **Option 3: Persona Team**
Use multiple personas together:
```yaml
personality:
  team:
    - romeo: promotion
    - luna: analytics  
    - buster: engagement
    - thomas: strategy
```

## 🔧 Implementation Examples:

### **In Skill Metadata:**
```yaml
metadata:
  personality:
    canine_personas:
      primary: luna
      rotation: [romeo, buster, thomas]
      enabled: true
```

### **In Content Generation:**
```python
def generate_with_persona(content, persona="romeo"):
    personas = {
        "romeo": "🐕 Romeo here! ",
        "luna": "📊 Luna analyzing: ",
        "buster": "💥 Buster reporting: ",
        "thomas": "🧠 Thomas reflecting: "
    }
    return f"{personas.get(persona, '')}{content}"
```

## 🎨 Visual Identity:

### **Emoji Mapping:**
- **Romeo:** 🐕✨🎉
- **Luna:** 🐕📊📈  
- **Buster:** 🐕💥🔥
- **Thomas:** 🐕🧠🌟

### **Color Scheme (Optional):**
- **Romeo:** Gold/Yellow
- **Luna:** Blue/Silver
- **Buster:** Red/Orange
- **Thomas:** Purple/Deep Blue

## 💡 Pro Tips:

1. **Be consistent** - if you start with Romeo, keep using Romeo
2. **Match persona to purpose** - Luna for data, Buster for action
3. **Don't overdo it** - use personas strategically, not constantly
4. **Let personas evolve** - based on community response

## 🚀 Getting Started:

```bash
# Test different personas
hermes run clawhub-test-persona --persona romeo --content "Welcome to our skill!"

# Set default persona for your skill
hermes run clawhub-set-persona --skill my-skill --persona luna

# Generate content with persona
hermes run clawhub-generate --persona buster --type feedback-request
```

**Remember: Personas make your skill relatable, not childish. Use them wisely.**
