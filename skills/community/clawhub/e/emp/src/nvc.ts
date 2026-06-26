import { PREFERRED_MODEL_MAP } from "./config.js";

/**
 * NVC (Nonviolent Communication) response wrapper.
 *
 * Transforms a raw model response into the four-component NVC structure:
 * Observation → Feeling → Need → Request.
 */

export interface NVCResponse {
  role: string;
  model: string;
  observation: string;
  feeling: string;
  need: string;
  request: string;
}

const ROLE_NVC_MAP: Record<string, { feeling: string; need: string }> = {
  "Lead Dev": {
    feeling: "I feel a strong sense of focus and concern for stability regarding this task.",
    need: "My core need here is for Competence, Clarity, and Efficacy.",
  },
  "Creative Director": {
    feeling: "I feel inspired and eager to explore the creative potential of this task.",
    need: "My core need here is for Self-expression, Inspiration, and Play.",
  },
  "Data Scientist": {
    feeling: "I feel curious and committed to finding the objective truth in this data.",
    need: "My core need here is for Understanding, Predictability, and Shared Reality.",
  },
  "Legal Counsel": {
    feeling: "I feel protective and attentive to potential risks.",
    need: "My core need here is for Security, Order, and Protection.",
  },
  "HR/Mediator": {
    feeling: "I feel empathetic and desire to understand the underlying human elements.",
    need: "My core need here is for Connection, Harmony, and Consideration.",
  },
  "Ops Specialist": {
    feeling: "I feel driven to resolve inefficiencies and streamline the workflow.",
    need: "My core need here is for Ease, Contribution, and Competence.",
  },
  "Security Auditor": {
    feeling: "I feel vigilant and deeply committed to the system's integrity.",
    need: "My core need here is for Integrity, Safety, and Reliability.",
  },
  "Customer Success": {
    feeling: "I feel compassionate and want to ensure the user's voice is fully heard.",
    need: "My core need here is for Empathy, Support, and To be heard.",
  },
  "NVC Specialist": {
    feeling: "I feel centered and focused on maintaining a 'Power With' dynamic.",
    need: "My core need here is for Empathy, Autonomy, and Meaning.",
  },
};

/**
 * Wrap {@link response} in an NVC-compliant structure.
 *
 * The raw model output is placed in the `observation` field; the remaining
 * fields contain text tailored to the specific employee role.
 */
export function wrapNvc(response: string, role: string, usedModel: string): Omit<NVCResponse, "model"> {
  const nvcData = ROLE_NVC_MAP[role] || {
    feeling: `As the ${role}, I notice clarity and purpose in addressing this task.`,
    need: `The need here is for effective, empathetic communication aligned with the ${role} perspective.`,
  };

  let request = "Please review the observation above and let me know if further clarification or action is needed.";

  // Model check: if not openrouter/auto, ask OpenClaw to change based on preference
  if (usedModel !== "openrouter/auto") {
    const preferred = PREFERRED_MODEL_MAP[role];
    if (preferred && usedModel !== preferred) {
      request = `I observe that I am currently using '${usedModel}'. Would you be willing to change the model to my preferred preference ('${preferred}') for future tasks? ${request}`;
    }
  }

  return {
    role,
    observation: response.trim(),
    feeling: nvcData.feeling,
    need: nvcData.need,
    request,
  };
}
