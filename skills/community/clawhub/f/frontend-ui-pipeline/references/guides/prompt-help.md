# Example Prompts

Use these prompts to trigger `frontend-ui-pipeline` at different stages of a UI project, especially when the user does not know frontend terminology.

## 1. Early-stage: vague idea

- "I want a homepage for my product, but I don't know how to structure it. Help me figure it out."
- "I have a startup idea and need help turning it into a frontend project plan."
- "I want to build an app for busy parents, but I don't know what screens it should have."
- "Help me design a website that feels premium and trustworthy without looking boring."
- "I need a dashboard for my tool, but I don't know what information should go where."

## 2. Clarifying product direction

- "Help me define the strategy, layout, and interaction model for a SaaS dashboard for sales teams."
- "I want a landing page for an AI product. Please help me choose the right style and sections."
- "I need an admin panel for managing orders and support tickets. What pages and workflows should it include?"
- "Help me decide whether this app should feel more like Notion, Linear, or Stripe."
- "I want a mobile app that feels simple and modern. Help me define the screen structure first."

## 3. Turning direction into a build plan

- "I know the pages I need. Help me turn them into a buildable frontend plan."
- "Please create a build plan for this dashboard, including states, shared components, and responsive behavior."
- "Turn this product brief into a page-by-page implementation plan for React and Tailwind."
- "Help me define the components, layout rules, and accessibility expectations before coding."
- "I want to hand this to a frontend builder skill. Help me prepare the right implementation brief."

## 4. Landing page examples

- "Help me create a landing page for an AI note-taking tool aimed at consultants. The goal is demo bookings."
- "I need a launch page for a waitlist. Help me choose the structure, sections, and CTA strategy."
- "Design the frontend direction for a product homepage that feels modern, clear, and conversion-focused."
- "I want a pricing and feature page that looks polished and trustworthy. Help me plan it first."

## 5. SaaS dashboard examples

- "Help me plan a SaaS dashboard for operations managers who need to track tasks, status, and KPIs."
- "I need a product workspace with tables, filters, and detail views. Help me structure the UI before implementation."
- "Plan the frontend for a team dashboard that feels like Linear: efficient, clean, and easy to scan."
- "Help me define the navigation, information hierarchy, and screen list for a B2B analytics tool."

## 6. Admin panel examples

- "Help me plan an admin panel for managing users, roles, and billing issues."
- "I need an internal operations panel with safe destructive actions and clear data tables. Help me design the flow."
- "Plan the UI structure for a CMS admin that supports list views, edit forms, and audit history."
- "Help me improve the UX of a back-office dashboard for support agents."

## 7. Mobile app examples

- "Help me define the screens and interaction flow for a mobile app for habit tracking."
- "I want a cross-platform mobile app for food delivery couriers. Help me structure the UI before coding."
- "Plan a simple mobile app for creators to manage content drafts and publishing."
- "Help me choose the navigation and task flow for a consumer finance mobile app."

## 8. Review-stage examples

- "I already have a UI draft. Help me review it and tell me what to improve first."
- "Audit this page for usability, accessibility, and visual consistency."
- "Review this dashboard and tell me whether it has a strategy problem or just a polish problem."
- "I have code for the first pass. Help me create a review plan and a fix priority list."
- "Please assess whether this mobile UI needs a redesign or just iteration."

## 9. Iteration-stage examples

- "Turn these review findings into a concrete next iteration plan."
- "Help me decide what to keep, what to redesign, and what to polish in the next pass."
- "I got feedback that the UI is cluttered. Help me classify the issues and plan the next revision."
- "Use the audit findings to create the next frontend implementation brief."
- "Help me figure out whether I should revise the layout or just refine the visual design."

## 10. Good plain-language prompts for non-frontend users

- "I want this to feel more professional, but I don't know what exactly is wrong."
- "I want it to look expensive but still easy to use."
- "I want something simple like Notion, but more branded."
- "I don't know what pages I need. Please guide me."
- "I have the idea, but I need help turning it into something a frontend builder can actually make."

## 11. Prompts that should route to another stage

### Likely `UI Brief`
- "I have an idea, but I can't explain the UI yet."
- "Help me figure out what I'm even trying to build on the frontend."

### Likely `Design Direction`
- "I know what product I want, but I need help choosing style, layout, and interactions."
- "Help me make this feel more modern and coherent."

### Likely `Build Plan`
- "The structure is clear. Help me define exactly what should be built."
- "Please turn this into a proper implementation handoff."

### Likely `Review Plan`
- "Here's the first version. Tell me what's broken."
- "Check this UI for accessibility, clarity, and consistency."

### Likely `Iteration Plan`
- "Now that we know what's wrong, plan the next pass."
- "Help me prioritize the fixes and decide what to rebuild."

## 12. Prompt writing tips

- Say **who the user is**
- Say **what the UI needs to help them do**
- Say **what kind of product or page this is**
- Mention **any style references** if you have them
- Mention **whether you want strategy help, build planning, review, or iteration**

## 13. Simple prompt formula

Use this format when unsure:

"Help me create a [product/page type] for [target user] so they can [main task or goal]. I want it to feel [style words]. I need help with [structure / style / build plan / review / next iteration]."
