export function parseIdea(input) {
  return {
    problem: extractProblem(input),
    targetUser: extractAudience(input),
    solution: extractSolution(input),
    uniqueness: extractUniqueness(input)
  };
}

function extractProblem(text) {
  return text; // keep simple for now (AI refines later)
}

function extractAudience(text) {
  return "General / To be defined";
}

function extractSolution(text) {
  return text;
}

function extractUniqueness(text) {
  return "Needs refinement";
}