// DASH_PATTERN detects only the two Unicode dash characters that are banned:
//   U+2013 EN DASH
//   U+2014 EM DASH
//
// Hyphen-minus (U+002D) is never touched.
// Double-hyphens (--) are fine and expected output.
export const DASH_PATTERN = /[\u2013\u2014]/;
// Correction prompt instructs the LLM to RESTRUCTURE, not just swap characters.
export const CORRECTION_PROMPT = "Rewrite the following text to eliminate all em-dashes (\u2014) and en-dashes (\u2013). " +
    "Restructure sentences so they read naturally without any dash characters. " +
    "Do not just swap dashes for commas or periods -- rephrase so the sentence flows properly. " +
    "Preserve the original meaning, tone, and length as closely as possible. " +
    "Do not add new content. Do not add explanations or preamble. " +
    "Output only the rewritten text.\n\nText to rewrite:\n";
//# sourceMappingURL=constants.js.map