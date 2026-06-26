# DentalBot Pro — WhatsApp Assistant for Dental Clinics

**24/7 AI receptionist that books appointments, answers patient questions, and grows your practice — all through WhatsApp.**

---

## The Problem

Dental clinics lose money every day to:

- **Missed calls** — 35% of patient calls go unanswered (ADA survey). Each missed call = $200-500 in lost revenue.
- **No-shows** — 15-20% of appointments are no-shows without reminders. At $150/appointment, a 10-appointment/day clinic loses $225-300/day.
- **Staff bottleneck** — Your receptionist spends 3-4 hours/day on calls that could be automated: scheduling, rescheduling, "what time do you open?", "do you take my insurance?"
- **After-hours silence** — 40% of patients look for dental care outside business hours. If they text you at 9 PM and get no response, they book with the clinic that does respond.
- **No reviews** — Most satisfied patients never leave a Google review because nobody asks. Your competitor with 200 reviews gets the new patients.

**The cost of doing nothing:** An average dental practice loses $8,000-12,000/month to these problems combined.

---

## The Solution

DentalBot Pro is an AI-powered WhatsApp assistant that handles 80% of patient interactions automatically, 24/7.

Your patients text your clinic's WhatsApp number. The bot responds instantly — scheduling appointments, answering questions, sending reminders, and requesting reviews. When it can't handle something, it seamlessly hands off to your staff.

**It's like hiring a receptionist who:**
- Never sleeps, never calls in sick, never takes lunch
- Speaks English and Portuguese fluently
- Responds in under 5 seconds, 24/7/365
- Never forgets to send reminders
- Asks every patient for a Google review
- Costs less than 1 hour of staff wages per day

---

## ROI Breakdown

| Metric | Before DentalBot | After DentalBot | Monthly Impact |
|--------|-----------------|-----------------|----------------|
| Missed calls → booked | 0 recovered | 15-25 recovered/mo | +$3,000-5,000 |
| No-show rate | 15-20% | 5-8% (with reminders) | +$1,500-2,250 saved |
| Staff hours on calls | 80 hrs/mo | 20 hrs/mo | +$1,500 saved (60 hrs) |
| After-hours bookings | 0 | 10-15/mo | +$2,000-3,000 |
| Google reviews | 1-2/mo | 8-15/mo | Long-term growth |
| **Total monthly impact** | | | **$8,000-12,250** |

**Your investment: $199-499/month.**

That's a **16x-62x ROI.**

---

## Pricing

| Plan | Price | Includes |
|------|-------|----------|
| **Starter** | $199/mo | 500 conversations/mo, scheduling, FAQ, reminders |
| **Professional** | $349/mo | 2,000 conversations/mo + Google Calendar sync + review requests |
| **Enterprise** | $499/mo | Unlimited conversations + multi-location + priority support + custom integrations |

All plans include: bilingual support (EN/PT), 24/7 operation, human handoff, setup assistance.

**14-day free trial. No credit card required. Cancel anytime.**

---

## Features

### Core
- **Appointment scheduling** — Patient texts, bot books. Syncs with Google Calendar.
- **Smart reminders** — 24h and 2h before appointments via WhatsApp. No-shows drop 60-70%.
- **Rescheduling & cancellation** — Patient texts to change, bot handles it. No phone tag.
- **FAQ auto-response** — Hours, insurance, parking, pricing, services. Instant answers.
- **New patient intake** — Collects name, phone, email, insurance via conversation. Ready when they arrive.

### Growth
- **Post-visit review requests** — Automated Google review request 2 hours after appointment.
- **After-hours coverage** — Books appointments at 3 AM. Never lose a patient to silence.
- **Bilingual (EN/PT)** — Detects language automatically. Responds in the patient's language.

### Safety
- **Emergency triage** — Detects urgent keywords, provides first-aid guidance, alerts staff immediately.
- **Human handoff** — Seamless escalation when the bot can't resolve. Staff gets full context.
- **HIPAA-conscious** — Never collects sensitive health data via chat. No medical diagnoses.
- **Privacy-first** — Conversations are confidential. No data shared between patients.

---

## Setup Guide (5 Minutes)

### Step 1: Connect WhatsApp (1 min)
Your WhatsApp Business number is connected to our platform. We provide the QR code — you scan it.

### Step 2: Customize Your Clinic Info (2 min)
Edit `config/faq-template.json` with your:
- Clinic name, address, phone
- Business hours
- Services and pricing ranges
- Insurance accepted
- Parking information
- Emergency number
- Google review link

### Step 3: Connect Google Calendar (2 min)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project (or use existing)
3. Enable **Google Calendar API**
4. Create a **Service Account** → download credentials JSON
5. Share your clinic's Google Calendar with the service account email (give "Make changes" permission)
6. Add the calendar ID and credentials path to `config/faq-template.json`

### Step 4: Test It
Send a WhatsApp message to your clinic number. The bot responds. Try:
- "I want to schedule an appointment"
- "What are your hours?"
- "Do you accept Delta Dental?"
- "Emergency"

### Step 5: Go Live
That's it. The bot is running 24/7.

---

## Demo Conversations

### Appointment Scheduling
```
Patient: Hi, I'd like to schedule a cleaning
Bot:     Great! What type of appointment would you like to schedule?
         • Cleaning & checkup
         • Whitening
         • Orthodontics consultation
         • Implant consultation
         • Emergency/pain
         • Other (please describe)

Patient: Cleaning and checkup
Bot:     What date and time work best for you?
         Our available hours are Mon-Thu 8AM-6PM, Fri 8AM-5PM, Sat 9AM-2PM.

Patient: Next Tuesday at 2pm
Bot:     To complete the booking, I'll need:
         1. Full name
         2. Email address

Patient: Sarah Johnson, sarah.j@email.com
Bot:     Perfect! Here's your appointment summary:
         📋 Service: Cleaning & Checkup
         📅 Date: Tuesday, March 17
         🕐 Time: 2:00 PM
         👤 Patient: Sarah Johnson
         Can I confirm this booking?

Patient: Yes!
Bot:     Your appointment is confirmed! ✅
         I'll send you a reminder 24 hours and 2 hours before.
         See you then!
```

### Portuguese Patient
```
Patient: Oi, quero agendar uma consulta
Bot:     Otimo! Que tipo de consulta voce gostaria de agendar?
         • Limpeza e revisao
         • Clareamento
         • Consulta ortodontia
         • Consulta implante
         • Emergencia/dor
         • Outro (descreva)

Patient: Clareamento
Bot:     Qual data e horario ficam melhor pra voce?
         Nossos horarios disponiveis sao Seg-Qui 8h-18h, Sex 8h-17h, Sab 9h-14h.

Patient: Sabado que vem de manha
Bot:     Sabado, 21 de marco as 9:00? Posso confirmar?
```

### Emergency
```
Patient: My tooth is broken and bleeding a lot
Bot:     I understand you're experiencing a dental emergency.

         🚨 Call our emergency line NOW: +1 (555) 123-9999

         While you wait:
         • For bleeding: Apply gentle pressure with gauze
         • For a broken tooth: Save any pieces, rinse gently
         • For pain: Over-the-counter ibuprofen can help

         If this is a life-threatening emergency, call 911 immediately.
         Our team has been notified and will prioritize your case.
```

### FAQ
```
Patient: Do you accept Cigna?
Bot:     Yes! We accept Cigna Dental. We also accept Delta Dental, MetLife,
         Aetna, United Healthcare, Guardian, Humana, and self-pay.
         Would you like to schedule an appointment?

Patient: How much is a whitening?
Bot:     Teeth whitening ranges from $300 to $800 depending on the treatment.
         Final pricing depends on your specific case and will be discussed
         during your consultation. Want me to schedule one?
```

---

## Technical Stack

- **AI Engine:** OpenClaw (Kraken) with GPT/Claude backend
- **Messaging:** WhatsApp Business API via OpenClaw
- **Calendar:** Google Calendar API (service account)
- **Hosting:** Runs on your existing OpenClaw instance
- **Config:** JSON files — no code needed to customize

---

## FAQ (For Clinic Owners)

**Q: Do I need technical knowledge?**
A: No. Setup is editing a JSON file with your clinic info. We provide templates.

**Q: What if the bot makes a mistake?**
A: The bot is designed to hand off to a human when uncertain. It never diagnoses, never gives medical advice, and always errs on the side of connecting with staff.

**Q: Is patient data safe?**
A: The bot never collects sensitive health information via chat. Patient data is handled following HIPAA-conscious practices. Conversations are encrypted end-to-end by WhatsApp.

**Q: Can I customize the messages?**
A: Yes. Edit `config/messages-template.json` to change any bot response. No coding required.

**Q: What about existing patients in my system?**
A: The bot works alongside your existing practice management software. It creates calendar events that sync with your workflow.

**Q: Multiple locations?**
A: Enterprise plan supports multiple locations, each with their own config and calendar.

---

## Support

- Setup assistance included in all plans
- Email: support@dentalbotpro.com
- Response time: < 4 hours during business hours
- Emergency technical support: 24/7 for Enterprise plans
