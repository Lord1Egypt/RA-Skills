---
description: Generate a professional branded proposal from brief job details. Input like "Mike, 2 acres, brush clearing, $4,600" and get a full proposal.
disable-model-invocation: true
---

# Proposal Generator

Read the user's business profile for company info, equipment list, and services.

## Input format
User says something like: "[name], [address], [acreage], [what needs done], [price]"
Or provides more detail. Work with whatever they give.

## Generate

### Header
Business name, address, phone, email, website from profile. Logo if available.

### Customer information
Name, property address, contact info (if provided)

### Property assessment
Turn the user's brief notes into professional language. Reference specific conditions, vegetation, terrain as described.

### Scope of work
- Specific services to be performed
- Equipment to be used (pull from their equipment list in profile)
- Expected timeline
- Access requirements

### What is NOT included
Standard exclusions: stump grinding below grade, hauling debris off-site, grading, seeding (unless specified). Customize to their services.

### Timeline
Estimated start date, duration, and completion. Note weather dependencies.

### Pricing
- Line items if multiple services
- Total price
- Payment terms: due upon completion (no deposit unless user specifies otherwise)
- Accepted payment methods from profile

### Terms and conditions
- Change orders require written approval and may adjust price/timeline
- Customer responsible for marking property lines, utilities, underground obstacles
- Cancellation policy: 48-hour notice
- Not responsible for damage to unmarked underground utilities
- Work area should be clear of vehicles, pets, personal items

### Signature block
Customer signature, date, printed name. Company signature line.

## Output format
Clean HTML that can be saved as PDF (Ctrl+P > Save as PDF). Use the business's brand colors if specified in profile.
