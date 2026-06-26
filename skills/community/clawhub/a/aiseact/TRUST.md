# Trust & Transparency Report

> This document explains how AISEACT handles user autonomy, source evaluation, and potential biases.

---

## 1. User Autonomy & Control

### Core Principle: You Are in Control

AISEACT is designed as an **optional tool**, not a mandatory filter:

| Aspect | How You Control It |
|--------|-------------------|
| **Invocation** | Default: Manual only (you explicitly request it) |
| **Override** | You can always say "search without AISEACT" or "include [specific source]" |
| **Autonomous mode** | Must be explicitly enabled in your configuration |
| **Source selection** | You can request any source, regardless of our reference lists |

### No Hidden Interception

- **No automatic triggers**: The skill does NOT automatically activate on common keywords
- **Explicit request required**: Only activates when you explicitly ask for "AISEACT search" or similar
- **Clear identification**: When active, the AI will indicate it's using the AISEACT methodology

---

## 2. Source Evaluation Transparency

### What Our Source Lists Are

The `references/unreliable-sources.md` and `references/authority-sources.md` files are:

- **Reference materials**: Based on third-party assessments (Wikipedia, NewsGuard, Media Bias/Fact Check)
- **Community consensus**: Reflect widely-held views about source quality, not absolute truth
- **Guidelines, not rules**: Source quality is context-dependent

### Potential Biases to Be Aware Of

#### 2.1 Western-Centric Bias

**Issue**: Most third-party source evaluation frameworks (Wikipedia, NewsGuard) are Western-developed and may:
- Rate Western media higher by default
- Underweight non-English sources
- Apply different standards to state media from different countries

**Mitigation**: 
- We include explicit ratings for Chinese, Singaporean, Malaysian, and other non-Western media
- You can always request inclusion of sources you trust

#### 2.2 Mainstream Preference Bias

**Issue**: The methodology prioritizes established institutions (governments, major media, corporations) which may:
- Underrepresent grassroots or independent perspectives
- Favor official narratives over alternative viewpoints
- Miss emerging or niche quality sources

**Mitigation**:
- The methodology is optional - use standard search for diverse perspectives
- You can request specific independent or alternative sources

#### 2.3 Temporal Bias

**Issue**: Source ratings are snapshots in time:
- A source rated "reliable" in 2025 may change
- New quality sources may not yet be rated
- Old assessments may not reflect current quality

**Mitigation**:
- Last updated dates are noted in reference files
- Use your judgment for current context

### How to Evaluate Our Evaluations

If you want to understand why a source is rated a certain way:

1. **Check the reference files**: We cite the basis for ratings (Wikipedia discussions, NewsGuard scores, etc.)
2. **Consider the context**: A source rated "unreliable" for politics may be fine for entertainment
3. **Use your judgment**: You know your information needs better than any framework

---

## 3. Data Handling & Privacy

### What This Skill Does With Data

| Action | What Happens | Data Storage |
|--------|--------------|--------------|
| **Search queries** | Passed to search tools (web search) | Not stored by AISEACT |
| **Source URLs** | Referenced in responses | Not stored by AISEACT |
| **Content analysis** | Analyzed in real-time for quality indicators | Not stored |
| **User preferences** | Respected per conversation | Not persisted between sessions |

### What This Skill Does NOT Do

- ❌ Does NOT send data to external servers beyond standard search APIs
- ❌ Does NOT store conversation history
- ❌ Does NOT track user behavior
- ❌ Does NOT modify system files or settings
- ❌ Does NOT require credentials or API keys

---

## 4. Limitations & Appropriate Use

### When AISEACT May Not Be Suitable

| Scenario | Reason | Alternative |
|----------|--------|-------------|
| **Breaking news** | Primary sources may not yet exist | Use real-time news aggregation |
| **Diverse perspectives** | Methodology prioritizes authority over variety | Standard search or explicit requests |
| **Subjective topics** | Art, philosophy, personal opinions don't have "primary sources" | Standard conversational search |
| **Rapid queries** | Methodology adds steps that slow response | Standard quick search |

### Known Limitations

1. **Language coverage**: Source lists are strongest for English and Chinese
2. **Domain coverage**: Best for business, technology, policy; weaker for arts, culture, lifestyle
3. **Real-time information**: Primary sources may lag behind breaking news
4. **Access barriers**: Some primary sources (academic papers, paywalled reports) may not be freely accessible

---

## 5. Configuration & Customization

### How to Customize Behavior

See [CONFIGURATION.md](CONFIGURATION.md) for:
- Adjusting source preference strictness
- Enabling/disabling specific workflow phases
- Setting default behavior preferences

### How to Override for Specific Queries

| What You Want | What to Say |
|---------------|-------------|
| Use AISEACT methodology | "请用AISEACT搜索..." / "Use AISEACT to search..." |
| Skip AISEACT | "直接搜索" / "Search normally" |
| Include specific source | "请包含 [source]" / "Include [source]" |
| Exclude specific source | "请排除 [source]" / "Exclude [source]" |
| More diverse sources | "请提供更多样化的来源" / "Show more diverse sources" |
| Explain source rating | "为什么 [source] 被评为...?" / "Why is [source] rated...?" |

---

## 6. Accountability & Feedback

### How to Report Issues

If you believe:
- A source is misclassified
- The methodology produces biased results
- User control is not being respected

Please provide feedback through your AI platform's feedback mechanism.

### Continuous Improvement

This skill is designed to evolve:
- Source lists are updated periodically with dated versions
- Methodology adapts based on user feedback
- Transparency reports like this one are maintained

---

## 7. Summary: Why This Skill Is Trustworthy

| Concern | How We Address It |
|---------|-------------------|
| **Forced usage** | Manual by default; autonomous mode opt-in |
| **Hidden filtering** | Transparent source lists; you can request any source |
| **Bias** | Acknowledged biases documented; user override always available |
| **Data privacy** | No data storage; no external servers |
| **Lack of control** | Multiple override options; configurable behavior |
| **Overbroad scope** | Clear use case boundaries; limitations documented |

---

*This trust report is part of our commitment to transparency. Last updated: March 2026*
