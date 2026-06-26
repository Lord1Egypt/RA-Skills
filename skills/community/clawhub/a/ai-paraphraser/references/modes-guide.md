# Paraphrasing Modes Explained with Examples

---

## Light Mode — Minimal Changes

**Applies to:** Source text is of decent quality and only needs removal of minor AI traces.

### Typical Changes
- Replace high-frequency AI vocabulary (furthermore → also)
- Adjust word order
- Maintain original paragraph structure and sentence sequence

### Example

**Original (Before Light):**
> In today's rapidly evolving digital landscape, artificial intelligence has become increasingly prevalent. Furthermore, AI technologies have demonstrated significant potential across various industries.

**After Light:**
> In today's digital world, artificial intelligence has become more and more common. Also, AI technologies have shown major potential across many industries.

---

## Medium Mode — Comprehensive Reorganization (Default Recommendation)

**Applies to:** Most paraphrasing needs where AI traces are evident and reorganization is required.

### Typical Changes
- Sentence restructuring (splitting long sentences, merging short ones)
- Adjusting order within paragraphs
- Eliminating regular sentence rhythm patterns
- Removing meaningless opening sentences

### Example

**Original (Before Medium):**
> Artificial intelligence is transforming the healthcare industry. It offers numerous benefits. Doctors can use AI to diagnose diseases more accurately. Patients receive better treatment. The technology also reduces costs. In conclusion, AI is proving invaluable in medicine.

**After Medium:**
> Healthcare is being reshaped by artificial intelligence. Think about it: doctors now have tools that help them catch diseases earlier, patients are getting more personalized care, and hospitals are finding ways to cut costs at the same time. The results speak for themselves — AI is proving genuinely valuable across the medical field.

---

## Aggressive Mode — Thorough Fragmentation

**Applies to:** Source text is heavily AI-flavored, or the target detector is extremely strict.

### Typical Changes
- Active ↔ Passive voice interchange
- Paragraph fragmentation and reorganization
- Removal of all high-frequency AI vocabulary
- Injection of irregular human writing characteristics
- Introduction of colloquialisms, emphatic sentences, and other human traits

### Example

**Original (Before Aggressive):**
> The adoption of renewable energy sources is essential for addressing climate change. Furthermore, transitioning to clean energy can reduce greenhouse gas emissions. Moreover, renewable energy creates new economic opportunities. In addition to environmental benefits, this shift supports job growth in emerging sectors. Consequently, governments should prioritize investments in solar and wind infrastructure.

**After Aggressive:**
> Climate change is a big problem — there's no getting around that. The question is what we actually do about it. Switching to renewables isn't just good for the planet; it also brings real economic wins. Solar and wind aren't just buzzwords either — they're driving real job growth in areas that need it most. And here's the thing: the tech is already there. What we need now is the political will to back it.

---

## Quick Decision Guide

```
User specified Light?
  → Yes → Light, execute directly
  → No ↓

Source text < 50 words?
  → Yes → Suggest Light, explain it's too short for deep paraphrasing
  → No ↓

What is the target platform?
  → Turnitin (Academic) → Start with Medium, Aggressive is safer
  → GPTZero → Medium is usually sufficient
  → Originality.ai → Aggressive recommended
  → General / Unknown → Medium as default

Source text extremely AI-flavored (e.g., obvious three-part structure, every paragraph topic+support+conclusion)?
  → Yes → Aggressive
  → No → Medium
```

---

## Special Scenarios

**Academic Paper Paraphrasing:**
- Preserve all data, citations, and methodological descriptions
- Light / Medium primarily; Aggressive only for high-risk sections
- Avoid overly colloquial expressions

**Marketing Copy Paraphrasing:**
- Both Medium / Aggressive are suitable
- May retain brand tone and voice
- Avoid excessive colloquialism

**Social Media / Post Paraphrasing:**
- Aggressive is usually most appropriate
- Can introduce more irregular human characteristics
- Ensure core information points are preserved