# Exam Stress Coach

**Manage exam anxiety with adaptive breathing exercises, evidence-based study planning, stress tracking, and motivational coaching.**

## The Real-World Problem

Exam anxiety affects **15–40% of students** (American Test Anxieties Association). High stress impairs working memory, reduces recall, and creates a vicious cycle: stress → poor performance → more stress. Most students have *no system* for managing this — they just push through, burn out, or resort to last-minute cramming that further increases anxiety.

Meanwhile, the tools that *do* exist (meditation apps, study planners) are disconnected. You track stress in one app, plan study in another, and do breathing in a third. **No single tool connects your stress level to what you should study and how.**

## Who Needs This

- **High school and university students** during finals, midterms, AP/IB, SAT/ACT, GRE, MCAT, bar exam
- **Parents** who want to support a stressed child with a structured plan
- **Adult learners** preparing for certification exams (PMP, CPA, CFA, AWS, etc.)
- **Teachers and tutors** who want to recommend a tool to anxious students
- **International students** facing high-stakes entrance exams under cultural pressure

## How It Works

Exam Stress Coach unifies five functions into one adaptive system:

1. **Stress Assessment** — Quick self-report (1–10) zones you into green/amber/red with tailored actions
2. **Breathing Studio** — Timed scripts for box breathing (4-4-4-4), 4-7-8 relaxation breath, and coherent breathing (5.5 breaths/min) — all backed by research on vagal tone and the parasympathetic nervous system
3. **Study Planner** — Spaced, interleaved schedules using distributed practice (Cepeda et al., 2008) with built-in rest and buffer days
4. **Stress Tracker** — JSON log + matplotlib trend visualization to see patterns over weeks
5. **Motivational Coach** — Evidence-based messages matched to your stress zone

## Quick Start

```bash
# Check in and get zone-based recommendations
python scripts/stress_coach.py assess --level 7

# 5-minute box breathing session
python scripts/stress_coach.py breathe --technique box --duration 5

# Create a 2-week study plan
python scripts/stress_coach.py plan --subjects "Calculus,History,Biology" --days 14 --hours-per-day 3
```

## Example Scenario

**Maya**, a university sophomore, has organic chemistry finals in 14 days. She's scoring 8/10 on stress.

1. **Assessment**: `assess --level 8` → RED zone. The coach says: *"Your stress is high. Before studying, let's bring it down. Run a 3-minute breathing exercise."*
2. **Breathing**: She runs `breathe --technique box --duration 3`. The script walks her through 4-4-4-4 cycles with visual cues.
3. **Study Plan**: `plan --subjects "Organic Chem" --days 14 --hours-per-day 3` → generates a JSON schedule with topics spaced across days, interleaved review, and the last 2 days reserved for full review only.
4. **Tracking**: Each day she logs `log --level N --note "..."`. After 2 weeks, `trend --days 14` shows her stress dropping from 8 to 4 as she gains control.

## Evidence Base

- **Box breathing** lowers cortisol and improves HRV (Lehrer & Gevirtz, 2021)
- **Distributed practice** doubles retention vs. massed practice (Cepeda et al., 2008)
- **Interleaving** improves problem-solving transfer (Rohrer & Taylor, 2007)
- **4-7-8 breathing** activates parasympathetic response (Weil, 2012)

See `references/techniques.md` for full citations.

## Installation

```bash
git clone https://github.com/voronindenis5/exam-stress-coach.git
cd exam-stress-coach
pip install matplotlib   # optional, for trend charts
```

## License

MIT — free for personal and educational use.
