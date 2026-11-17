// What the second live contact search looks for: every identity key the first
// search's records carry, so a group no single key spans is gathered whole
// before anything is scored.

import { defineScript } from "@cargo-ai/cdk";

import { unique } from "../common/values";
import { type Contact, readContacts } from "./contact";
import { linkedinUrlVariants } from "./identity";

export const prepareTransitiveContactSearch = defineScript(
  ({ records }: { records: unknown }) => {
    const contacts = readContacts(records);

    return {
      linkedinPersonIds: keysOf(contacts, "linkedinPersonId"),
      linkedinUrlVariants: unique(
        contacts.flatMap((contact) => linkedinUrlVariants(contact.linkedinUrl)),
      ),
      emails: keysOf(contacts, "email"),
      phones: keysOf(contacts, "phone"),
    };
  },
);

const keysOf = (
  contacts: Contact[],
  key: "linkedinPersonId" | "email" | "phone",
): string[] => {
  return unique(
    contacts
      .map((contact) => contact[key])
      .filter((value): value is string => value !== undefined),
  );
};
