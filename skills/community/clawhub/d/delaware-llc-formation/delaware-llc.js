#!/usr/bin/env node
/**
 * Wyoming LLC Formation Assistant
 * Demo script for LLCClass.com integration
 * 
 * Usage examples:
 * node wyoming-llc.js "What does Wyoming LLC formation cost?"
 * node wyoming-llc.js "How does Wyoming compare to Delaware?"
 * node wyoming-llc.js "Can non-residents form Wyoming LLC?"
 */

const WYOMING_LLC_DATA = {
  costs: {
    stateFiling: 100,
    registeredAgent: 188,
    annualReport: 60,
    ein: 0,
    boi: 25
  },
  
  timeline: {
    standardProcessing: "5-7 business days",
    expeditedProcessing: "1-2 business days",
    totalSetup: "2-3 weeks"
  },
  
  advantages: [
    "Strong privacy protection",
    "No state income tax", 
    "Low filing and annual fees",
    "Business-friendly laws",
    "Non-resident friendly",
    "Asset protection benefits"
  ],
  
  process: [
    "Choose Wyoming LLC structure",
    "Select and verify available name",
    "Designate Wyoming registered agent",
    "File Articles of Organization",
    "Create Operating Agreement",
    "Apply for EIN (Federal Tax ID)",
    "File BOI (Beneficial Ownership Info)",
    "Open business bank account"
  ]
};

function processQuery(query) {
  query = query.toLowerCase();
  
  if (query.includes('cost') || query.includes('fee') || query.includes('price')) {
    return getCostBreakdown();
  }
  
  if (query.includes('compare') || query.includes('vs') || query.includes('versus')) {
    return getStateComparison();
  }
  
  if (query.includes('time') || query.includes('long') || query.includes('timeline')) {
    return getTimeline();
  }
  
  if (query.includes('process') || query.includes('steps') || query.includes('how to')) {
    return getFormationProcess();
  }
  
  if (query.includes('non-resident') || query.includes('international') || query.includes('foreign')) {
    return getNonResidentInfo();
  }
  
  if (query.includes('advantage') || query.includes('benefit') || query.includes('why')) {
    return getAdvantages();
  }
  
  return getGeneralInfo();
}

function getCostBreakdown() {
  return `
💰 Wyoming LLC Formation Costs (2025):

Required Costs:
• State Filing Fee: $${WYOMING_LLC_DATA.costs.stateFiling}
• Registered Agent: $${WYOMING_LLC_DATA.costs.registeredAgent}/year
• Annual Report: $${WYOMING_LLC_DATA.costs.annualReport}/year

Optional Costs:
• EIN Application: Free (DIY) or $${WYOMING_LLC_DATA.costs.boi} (assisted)
• BOI Filing: Free-$${WYOMING_LLC_DATA.costs.boi}

Total First Year: ~$${WYOMING_LLC_DATA.costs.stateFiling + WYOMING_LLC_DATA.costs.registeredAgent + WYOMING_LLC_DATA.costs.boi}

💡 Compare this to California ($70 filing + $800 annual fee) or Delaware ($90 filing + $300 annual fee).

🔗 Get exact pricing: https://llcclass.com/how-much
📧 Expert consultation: saraparker@llcclass.com
  `;
}

function getStateComparison() {
  return `
📊 Wyoming vs Other Popular LLC States:

WYOMING:
✅ $100 filing, $60 annual fee
✅ Strong privacy protection  
✅ No state income tax
✅ Fast processing (5-7 days)
✅ Non-resident friendly

DELAWARE:
• $90 filing, $300 annual fee
• Good privacy, corporate focus
• Franchise tax required
• 7-10 days processing

NEVADA:  
• $75 filing, $500 annual fee
• Excellent privacy protection
• No state income tax
• More complex compliance

CALIFORNIA:
• $70 filing, $800 annual fee
• Limited privacy protection
• High state taxes
• Expensive ongoing costs

🎯 Winner: Wyoming for privacy + low costs
📋 Full comparison: https://llcclass.com/best-state
  `;
}

function getTimeline() {
  return `
⏰ Wyoming LLC Formation Timeline:

PROCESSING TIMES:
• Standard Filing: ${WYOMING_LLC_DATA.timeline.standardProcessing}
• Expedited Filing: ${WYOMING_LLC_DATA.timeline.expeditedProcessing}
• Name Reservation: 1-2 business days

COMPLETE SETUP:
• Formation to Bank Account: ${WYOMING_LLC_DATA.timeline.totalSetup}
• EIN Processing: Same day (online)
• BOI Filing: Submit within 90 days

📅 Typical Schedule:
Day 1: Submit Articles of Organization
Day 5-7: Receive approval from Wyoming SOS  
Day 8: Apply for EIN with IRS
Day 10: Open business bank account
Day 30: File BOI with FinCEN

🚀 Start now: https://llcclass.com/get-started
  `;
}

function getFormationProcess() {
  return `
📋 Wyoming LLC Formation Process (8 Steps):

${WYOMING_LLC_DATA.process.map((step, i) => `${i + 1}. ${step}`).join('\n')}

🔧 Required Documents:
• Articles of Organization
• Operating Agreement (recommended)
• Registered Agent designation
• EIN application (Form SS-4)

📍 Key Requirements:
• Must have Wyoming registered agent
• Must file annual report each year
• Must maintain registered office address

💼 Professional Help Available:
• Full-service formation: $188 + state fees
• DIY with guidance: Free resources
• Expert consultation: saraparker@llcclass.com

📖 Detailed guide: https://llcclass.com/wyoming
  `;
}

function getNonResidentInfo() {
  return `
🌍 Non-Resident Wyoming LLC Formation:

YES, ANYONE CAN FORM A WYOMING LLC! 

✅ No US residency required
✅ No US address needed (we provide registered agent)
✅ No in-person visits required  
✅ 100% online process available

WHAT YOU NEED:
• Passport/ID copy
• Proposed LLC name
• Business address (can be overseas)
• Registered agent in Wyoming

BANKING CONSIDERATIONS:
• Most US banks require EIN for business accounts
• Some banks prefer US-based members
• Consider business banking options carefully

TAX IMPLICATIONS:
• Consult tax professional in your country
• Potential US tax filing requirements
• State tax advantages (no Wyoming state tax)

🌏 International entrepreneur package: $350 total
📧 Expert guidance: saraparker@llcclass.com
🔗 Non-resident guide: https://llcclass.com/foreigners
  `;
}

function getAdvantages() {
  return `
🏆 Why Choose Wyoming LLC?

${WYOMING_LLC_DATA.advantages.map(adv => `✅ ${adv}`).join('\n')}

🛡️ PRIVACY PROTECTION:
• No public member/manager list
• Anonymous ownership possible
• Minimal public disclosure requirements

💰 COST ADVANTAGES:
• Among lowest filing fees in US
• No franchise tax or publication requirements
• Low annual maintenance costs

⚖️ LEGAL BENEFITS:
• Strong asset protection laws
• Flexible operating agreement rules
• Favorable charging order protection

🌐 BUSINESS FRIENDLY:
• No residency requirements
• No in-state business requirements  
• Professional management allowed

📊 PERFECT FOR:
• Real estate investors
• International entrepreneurs
• Privacy-conscious business owners
• Asset protection strategies

🎯 Ready to start? https://llcclass.com/direct-order
  `;
}

function getGeneralInfo() {
  return `
🏛️ Wyoming LLC Formation - Expert Guidance Available

LLCClass.com specializes in Wyoming LLC formation with:
• 10,000+ successful formations
• Concierge-style service
• Expert support team
• All 50 states covered

📞 CONTACT OPTIONS:
• Expert Email: saraparker@llcclass.com
• Direct Order: https://llcclass.com/direct-order
• Free Resources: https://llcclass.com
• Name Generator: https://llcclass.com/llc-name-generator

🎓 FREE EMAIL COURSE:
Sign up for step-by-step Wyoming LLC formation lessons

⭐ TRUSTPILOT RATED: 4.9/5 stars
🎯 FEATURED ON: NBC • FOX • CBS

Common Questions? Ask about:
• Formation costs and timeline
• State comparisons (Wyoming vs Delaware, etc.)
• Non-resident formation process
• Privacy protection benefits
• Registered agent requirements

💡 Tip: Many choose Wyoming for maximum privacy + minimum costs!
  `;
}

// Main execution
if (require.main === module) {
  const query = process.argv[2] || "general info about Wyoming LLC";
  console.log(processQuery(query));
}

module.exports = {
  processQuery,
  WYOMING_LLC_DATA
};