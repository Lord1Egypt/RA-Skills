// What the first live contact search looks for: the enrolled row's own identity
// keys, in the forms a CRM could have stored them.

import { defineScript } from "@cargo-ai/cdk";

import { linkedinUrlVariants, normalizeEmail } from "./identity";

export const prepareContactSearch = defineScript(
  ({
    sourceId,
    linkedinPersonId,
    linkedinUrl,
    email,
    phone,
  }: {
    sourceId: string;
    linkedinPersonId: string | undefined;
    linkedinUrl: string | undefined;
    email: string | undefined;
    phone: string | undefined;
  }) => {
    return {
      sourceId,
      linkedinPersonId,
      // A search matches stored text, so each URL form is searched separately.
      linkedinUrlVariants: linkedinUrlVariants(linkedinUrl),
      email: normalizeEmail(email),
      // Searched exactly as stored: a phone number's variants cannot be
      // enumerated, so they pair records in a cluster rather than gather one.
      phone,
    };
  },
);
