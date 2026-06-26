import { research } from "./web_research.js";

export async function generateStrategy(idea, context = {}) {

  const queries = [
    `${idea.problem} competitors`,
    `${idea.problem} market size`,
    `${idea.problem} startup case studies`,
  ];

  let researchData = [];

  for (let q of queries) {
    try {
      const res = await research(q, context);
      researchData.push(res);
    } catch (e) {}
  }

  const competitors = extractCompetitors(researchData);
  const differentiation = buildDifferentiation(idea, competitors);
  const gtm = buildChannelGTM(idea);
  const economics = buildEconomics(idea);
  const pricing = buildPricing(idea);

  return {
    competitors,
    differentiation,
    gtm,
    economics,
    pricing
  };
}

// -----------------------------

function extractCompetitors(data) {
  return data.map(d => ({
    name: "Detected Competitor",
    strength: "Strong market presence",
    weakness: "Generic offering"
  }));
}

// -----------------------------

function buildDifferentiation(idea, competitors) {
  return {
    positioning: "Focus on niche + stronger UX + speed",
    advantage: "Combine entertainment + utility",
    gap: "Competitors lack engagement loops"
  };
}

// -----------------------------

function buildChannelGTM(idea) {
  return {
    instagram: {
      strategy: "Reels + meme content",
      goal: "viral reach",
    },
    reddit: {
      strategy: "problem-first posts",
      goal: "early adopters",
    },
    youtube: {
      strategy: "explainer + storytelling",
      goal: "trust building",
    }
  };
}

// -----------------------------

function buildEconomics(idea) {
  return {
    CAC: "Low initially via organic",
    LTV: "High if retention achieved",
    ratio: "Target > 3:1",
    note: "Focus on retention before scaling paid ads"
  };
}

// -----------------------------

function buildPricing(idea) {
  return {
    model: "Freemium",
    entry: "Free hook",
    upgrade: "Premium features",
    expansion: "Subscriptions + add-ons"
  };
}