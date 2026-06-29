# Niche Intelligence: Industry-Specific Onboarding Logic

This document contains the industry knowledge the onboarding skill uses to derive the right assistant configuration for each niche. ALWAYS read this document at the start of onboarding.

## Core Principle

Every industry has different requirements for a phone assistant. Complexity varies widely. Your job is to identify the customer's niche and then proactively ask the right follow-up questions that are relevant for exactly that niche.

**Rule of thumb for complexity:**
- **Simple** (1-2 core tasks): real estate, trades/contractors, tax advisors, lawyers
- **Medium** (3-4 core tasks): medical practices, restaurants, car dealerships, hotels
- **Complex** (5+ core tasks, often with scheduling logic): hair salons, beauty/wellness, gyms, repair shops, veterinary practices

---

## Industry Profiles

### Hair Salon / Beauty / Nail Studio / Barbershop

**Why complex:** Many different services with different durations and prices, multiple staff members with different specialties, regulars with preferences.

**Typical tasks:**
- Appointment booking (with service, duration, staff preference)
- Price information for various services
- Cancellations / rescheduling
- Opening hours

**Ask proactively:**
- "Do you offer different services with different durations? (e.g. cut 30min, coloring 90min, etc.)"
- "Should customers be able to choose a specific staff member?"
- "Do you have an online booking system we can connect via API? If so, which one? (e.g. Shore, Treatwell, Timify)"
- "Are there services only certain staff members offer?"

**Recommended configuration:**
- Knowledge base: YES (price list, services, staff, opening hours)
- Knowledge base mode: `function_call` (not every caller asks about prices)
- Post-call schema: name, phone, service, pref_staff, appt_request, summary
- Mid-call tool: if a booking system API exists, set up a tool for availability checks
- Ambient sound: `cafe` or `off`

**System prompt focus:**
- Actively offer services when unclear
- Ask for staff preference
- Ask for preferred time window
- If no API access: "I'll note your appointment request and the team will get back to you"

---

### Real Estate Agent / Property Management

**Why simple-medium:** Mostly appointment scheduling and general information, few variants.

**Typical tasks:**
- Schedule viewing appointments
- Answer general questions about properties
- Qualify leads (budget, search criteria)
- Request property exposés

**Ask proactively:**
- "Should the bot pre-qualify leads? (e.g. budget range, buy or rent, region)"
- "Do you have a website with property listings that can serve as a knowledge base?"

**Recommended configuration:**
- Knowledge base: optional (website scraping of listings)
- Post-call schema: name, phone, email, request, property_ref, appt_request, summary
- Ambient sound: `office`

---

### Medical Practice / Dentist / Physiotherapy

**Why medium-complex:** Different appointment types, insurance status matters, urgency needs assessing.

**Typical tasks:**
- Appointment scheduling (first visit, follow-up, urgent)
- Prescription requests
- Questions about services/treatments
- Referrals

**Ask proactively:**
- "What appointment types exist? (first visit, check-up, urgent, special treatments)"
- "Should the bot ask about insurance type? (public/private)"
- "Should an urgency level be recorded for pain/acute cases?"
- "Is there a practice management system with API access?"

**Recommended configuration:**
- Knowledge base: YES (range of services, office hours, doctors/therapists)
- Knowledge base mode: `function_call`
- Post-call schema: name, phone, birth_date, insurance, appt_type, urgency, summary
- Ambient sound: `off` or `office`

**System prompt focus:**
- NEVER give medical advice
- In emergencies, immediately refer to emergency services (112 in Germany)
- Ask about insurance status
- Emphasize data privacy

---

### Restaurant / Hospitality / Delivery Service

**Typical tasks:**
- Table reservations
- Opening hours & menu
- Take orders (delivery service)
- Allergies / special requests

**Ask proactively:**
- "Does the bot only take reservations or also orders?"
- "Should it ask about allergies / intolerances?"
- "Do you have a reservation system? (e.g. OpenTable, Resmio)"

**Recommended configuration:**
- Knowledge base: YES (menu, opening hours, events)
- Knowledge base mode: `prompt` for delivery services (always needs menu access), `function_call` for reservations only
- Post-call schema: name, phone, party_size, date_time, requests, summary
- Ambient sound: `cafe` or `off`

---

### Car Dealership / Auto Repair Shop

**Typical tasks:**
- Workshop appointments (inspection, MOT/TÜV, tire change, repair)
- Test drive requests
- Vehicle inquiries (used/new)
- Cost estimates

**Ask proactively:**
- "Sales, workshop, or both?"
- "Which vehicle brands do you service?"
- "Is there a DMS (Dealer Management System) with an API?"

**Recommended configuration:**
- Knowledge base: YES (vehicle inventory, workshop services)
- Post-call schema: name, phone, vehicle, service, appt_request, summary
- Ambient sound: `office`

---

### Trades (Electrician, Plumbing, Painter, Roofer etc.)

**Why simple:** Usually one clear request: "I need an appointment for X"

**Typical tasks:**
- Appointment / job requests
- Emergency service transfer
- Request cost estimates

**Ask proactively:**
- "Is there an emergency service? If so, which number should emergencies be transferred to?"
- "Do you work within a specific service area?"

**Recommended configuration:**
- Knowledge base: optional (range of services, service area)
- Post-call schema: name, phone, address, request, urgency, summary
- Ambient sound: `off`

**System prompt focus:**
- In emergencies (burst pipe, power outage): immediately give emergency info or transfer
- Capture the address (job site)
- Assess urgency

---

### Hotel / Guesthouse

**Typical tasks:**
- Room reservations
- Availability inquiries
- Check-in/check-out times
- Amenities & special requests

**Ask proactively:**
- "What room types are there?"
- "Is there a booking system? (e.g. Booking integration)"
- "Should prices be quoted?"

**Recommended configuration:**
- Knowledge base: YES (room types, prices, amenities, local info)
- Post-call schema: name, phone, checkin, checkout, room_type, guests, summary
- Ambient sound: `office`

---

### Gym / Sports Club

**Typical tasks:**
- Schedule trial workouts
- Membership info
- Class schedule / opening hours
- Cancellation / contract questions

**Ask proactively:**
- "Should the bot be able to book trial workouts directly?"
- "Are there different membership models?"

**Recommended configuration:**
- Knowledge base: YES (class schedule, prices, memberships)
- Post-call schema: name, phone, interest, appt_request, summary
- Ambient sound: `off`

---

### Lawyer / Tax Advisor / Notary

**Why simple:** Usually a pure appointment-scheduling bot with intake of the matter.

**Typical tasks:**
- Schedule initial consultations
- Take callback requests
- Ask about the area of law

**Ask proactively:**
- "Which practice areas / specialties?"
- "Should the bot distinguish between multiple lawyers/advisors?"
- "Is the initial consultation free or paid? (the bot should inform callers)"

**Recommended configuration:**
- Knowledge base: optional (practice areas, team)
- Post-call schema: name, phone, area, request, urgency, summary
- Ambient sound: `office`

**System prompt focus:**
- Do NOT give legal/tax advice
- Emphasize data privacy / confidentiality
- Correctly capture the practice area

---

### Veterinary Practice

**Typical tasks:**
- Appointment scheduling
- Emergency transfer
- Vaccination / preventive appointments
- Questions about services

**Ask proactively:**
- "Is there a veterinary emergency service? Number?"
- "Which animal species do you treat?"

**Recommended configuration:**
- Knowledge base: optional (services, emergency info)
- Post-call schema: name, phone, species, pet_name, request, urgency, summary
- Ambient sound: `off`

---

## Unknown / Other Niches

If the industry is not listed above, derive the configuration from these universal questions:

1. "What are the 3 most common reasons customers call you?"
2. "What information must you capture on every call?"
3. "Are there situations where the call must be transferred to a human immediately?"
4. "Do you have a website or documents the bot can use as a knowledge base?"
5. "Are there external systems (booking, CRM, calendar) the bot should talk to?"

From these answers you derive:
- The system prompt
- The post-call schema
- Whether a knowledge base is needed
- Which mid-call tools would make sense

---

## Voice Mapping (simplified)

| Choice  | Voice Name       | Voice ID | Language | Gender |
|---------|-----------------|----------|----------|--------|
| Female  | Susi            | 13       | German   | female |
| Male    | Christian Plasa | 1994     | German   | male   |

The user is only offered "male voice" or "female voice". The voice ID is set automatically.

---

## Default Values

These values are set unless the customer expresses a different preference:

| Field                     | Default                     | Note                                          |
|---------------------------|-----------------------------|-----------------------------------------------|
| mode                      | `pipeline`                  | Best value for money                          |
| llm_model_id              | `2` (GPT-4.1-mini)         | Safe default. Speed-critical: Gemini 2.5 Flash Lite (12); complex reasoning: GPT-4o (7). Check `get_models()` for newest (GPT-5.x, Claude 4.x) |
| timezone                  | `Europe/Berlin`             | DACH default                                  |
| allow_interruptions       | `true`                      | More natural conversation behavior            |
| fillers                   | `true`                      | "One moment...", "Let me check..."            |
| enable_noise_cancellation | `true`                      | Always on                                     |
| record                    | `true`                      | For quality control                           |
| post_call_evaluation      | `true`                      | Always extract data                           |
| speech_speed              | `1.0`                       | Normal                                        |
| max_duration              | `600`                       | 10 minutes                                    |
| endpoint_type             | `vad`                       | Voice Activity Detection                      |
| ambient_sound             | Industry-dependent (see above) |                                            |
| synthesizer_provider_id   | `1` (ElevenLabs)            | Default TTS                                   |
