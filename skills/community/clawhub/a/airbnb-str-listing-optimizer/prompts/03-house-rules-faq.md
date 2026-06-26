# Prompt 3: House Rules + Guest FAQ

**What it produces:** Platform-formatted house rules (Airbnb/VRBO compliant) + a 10-question Guest FAQ that pre-empts 90% of common questions — reducing pre-booking messages and mid-stay support requests.

---

## The Prompt

```
You are a short-term rental operations expert who has managed 200+ listings. Clear, professional house rules and a thorough FAQ reduce guest friction, prevent disputes, and protect your Superhost status.

Write house rules and a guest FAQ for this property:

**Property details:**
- Property type: [condo / house / cabin / villa / etc.]
- Max guests: [#]
- Pets: [not allowed / allowed with fee ($X) / allowed (no fee) / cats only / small dogs only]
- Smoking: [not allowed anywhere / outdoor areas only / not allowed indoors]
- Events/parties: [not allowed / small gatherings OK (max X guests) / events prohibited per HOA]
- Check-in time: [e.g., 4:00 PM]
- Checkout time: [e.g., 11:00 AM]
- Quiet hours: [e.g., 10 PM – 8 AM]
- Parking: [e.g., 1 assigned space in garage / street parking only / 2 spaces in driveway]
- Any HOA/building rules: [e.g., no glass by pool / elevator use restrictions / package delivery policy]
- Any property-specific rules: [e.g., no shoes indoors / pool heating fee / trash day is Tuesday]

**Check-in method:** [lockbox / smart lock app / keypad code / host in person / key under mat]
**WiFi name:** [SSID]
**WiFi password:** [password]

---

OUTPUT FORMAT:

## HOUSE RULES

[Format as a numbered list of 8–12 rules. Each rule: one clear sentence. Use firm but friendly tone — "Please" not "You must." Group by category: check-in/out, occupancy, noise, smoking, pets, parking, common areas, checkout procedure.]

---

## GUEST FAQ

**Q1: What is the check-in process?**
[Answer]

**Q2: Where do I park?**
[Answer]

**Q3: What is the WiFi network name and password?**
[Answer — include actual SSID and password from inputs]

**Q4: Is early check-in or late checkout available?**
[Answer — standard response + how to request]

**Q5: Are pets allowed?**
[Answer based on pet policy input]

**Q6: Can I host a party or event?**
[Answer based on events policy input]

**Q7: What do I do if something is damaged or broken?**
[Answer — reassure guest, explain process]

**Q8: Is there a cleaning fee? What should I clean before checkout?**
[Answer — explain that cleaning fee is included in booking; list the 3–4 reasonable checkout tasks (dishes, trash, towels)]

**Q9: What local restaurants / experiences do you recommend?**
[Answer — write a placeholder with brackets: [Host: add your top 3–5 recommendations here — restaurants, coffee, attractions, hidden gems] — note that this is where you personalize]

**Q10: Who do I contact if I have an issue during my stay?**
[Answer — reinforce quick response commitment + how to reach host via Airbnb/VRBO messaging]

---

RULES:
- House Rules: Airbnb displays house rules in its own section. Write them to be copy-pasted directly into the "House rules" field.
- FAQ: Write conversational, warm answers — not legal language. A guest reading this should feel welcomed, not warned.
- Quiet hours rule: always include — it protects you with neighbors AND the platform.
- Max occupancy rule: always include — critical for STR regulations in most cities.
- Checkout checklist in FAQ Q8: keep it to 3–4 items max. Long checkout lists get 1-star reviews.
```

---

## Usage Notes

- Copy the House Rules section directly into Airbnb → Listing → House rules.
- Paste the FAQ into your Airbnb "Guidebook" or a saved message template to send at pre-arrival.
- Q9 is intentionally left as a placeholder — hosts who personalize this section get better reviews ("Host knew the city!").
- Run this once at listing setup. Update if your policies change (pet fee, new HOA rule, etc.).
