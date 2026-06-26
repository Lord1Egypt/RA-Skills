# Industry Adaptation Guide (Tiered Loading Router)

This file serves as the entry point for industry adaptation. To optimize context load, specific industry SOPs are split into the `industries/` sub-directory.

---

## 1. Industry Routing Table

| Industry | Core Sub-module Path | Content Overview |
| :--- | :--- | :--- |
| **F&B/Retail** | `references/industries/catering.en.md` | Image upgrade, Opening SOP, F&B redlines |
| **E-commerce/Digital** | `references/industries/digital.en.md` | Site building, Private traffic, Data tracking, Compliance |
| **Manufacturing** | `references/industries/manufacturing.en.md` | Line renovation, Quality systems, ERP/MES |
| **Education** | `references/industries/education.en.md` | Curriculum R&D, Platform setup, Campus compliance |
| **Events** | `references/industries/events.en.md` | PR events, Product launches, Police approvals |
| **Real Estate** | `references/industries/real-estate.en.md` | Development, Prefab standards, Permit redlines |
| **Live Streaming** | `references/industries/livestream.en.md` | Studio setup, GMV padding, Influencer risk |
| **Urban Renewal** | `references/industries/urban-renewal.en.md` | Structural加固, Heritage redlines, Unforeseen costs |
| **Exhibition** | `references/industries/exhibition.en.md` | Showroom design, SI standardization, Multimedia integration |
| **Consulting** | `references/industries/consulting.en.md` | Strategic consulting, Tourism plans, ROI models |
| **Healthcare** | `references/industries/healthcare.en.md` | Smart health, GSP compliance, Data privacy |
| **Fintech** | `references/industries/fintech.en.md` | IT innovation, Risk models, Data consistency |
| **Government** | `references/industries/government.en.md` | G2B services, Data lakes, Prime contractor audit |

---

## 2. Cross-Industry Rules

1. **Determine Prime Industry**: Use the industry of the core deliverable as the main framework.
2. **Tiered Loading**: Load the prime industry file first, then the auxiliary industry file if needed.
3. **Role Merging**: Combine overlapping roles across sectors.
4. **Conflict Resolution**: If processes conflict, prioritize the prime industry's flow.
