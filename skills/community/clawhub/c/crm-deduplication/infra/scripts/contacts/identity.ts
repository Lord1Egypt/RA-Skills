// How one person's identity keys are read, so two records written by different
// people still read as the same person. Every comparison on the contact path
// goes through these, and the audit has to normalize the same way: a difference
// here shows up as a duplicate the audit counted and the play never merges.

import { asText, unique } from "../common/values";
import { GENERIC_EMAIL_LOCAL_PARTS } from "./policy";

/** An email address, case-folded. */
export const normalizeEmail = (value: unknown): string | undefined => {
  return asText(value)?.toLowerCase();
};

/**
 * A LinkedIn profile read as the handle LinkedIn addresses the person by:
 * `jack-smith`, whether the CRM stored the bare handle, `http://`, `www.`, a
 * tracking query, or a trailing slash.
 */
export const normalizeLinkedinProfile = (
  value: unknown,
): string | undefined => {
  const handle = asText(value)
    ?.toLowerCase()
    .replace(/^(?:https?:\/\/)?(?:[\w-]+\.)?linkedin\.com\/in\//, "")
    .replace(/[?#].*$/, "")
    .replace(/\/+$/, "");
  return handle === "" ? undefined : handle;
};

/**
 * The URL forms a CRM could hold for one profile. A CRM search matches stored
 * text, not normalized text, so the play searches all four rather than the one
 * form this code prefers.
 */
export const linkedinUrlVariants = (value: unknown): string[] => {
  const handle = normalizeLinkedinProfile(value);
  if (handle === undefined) {
    return [];
  }

  return [
    `https://linkedin.com/in/${handle}`,
    `https://linkedin.com/in/${handle}/`,
    `https://www.linkedin.com/in/${handle}`,
    `https://www.linkedin.com/in/${handle}/`,
  ];
};

/**
 * A phone number in E.164 when the stored value says which country it belongs
 * to: an explicit `+`, an international `00` prefix, or a national number with
 * no trunk prefix that NANP can claim. Anything else stays as its digits —
 * a country code is not something this can invent.
 */
export const normalizePhone = (value: unknown): string | undefined => {
  const stored = asText(value);
  if (stored === undefined) {
    return undefined;
  }

  const digits = digitsOf(stored);
  if (digits === "") {
    return undefined;
  }
  if (stored.startsWith("+")) {
    return `+${digits}`;
  }
  if (hasInternationalPrefix(digits)) {
    return `+${digits.slice(2)}`;
  }
  if (isNorthAmerican(digits)) {
    return `+1${digits.slice(-10)}`;
  }
  return digits;
};

/**
 * Every form of one stored phone number that another record could hold, used to
 * pair records a search already returned. A search cannot enumerate these, so a
 * number kept with its national trunk prefix only pairs inside a cluster the
 * other keys already gathered.
 */
export const phoneMatchKeys = (value: unknown): string[] => {
  const digits = digitsOf(value);
  if (digits === "") {
    return [];
  }

  const keys = [normalizePhone(value), digits];
  if (hasInternationalPrefix(digits)) {
    keys.push(`+${digits.slice(2)}`);
  }
  // A number kept with its national trunk `0` is the same line as its E.164
  // form. France and the UK are the defaults; add the country codes the audited
  // CRM actually holds.
  if (hasTrunkPrefix(digits)) {
    if (digits.length === 10) {
      keys.push(`+33${digits.slice(1)}`);
    }
    keys.push(`+44${digits.slice(1)}`);
  }
  if (isNorthAmerican(digits)) {
    keys.push(`+1${digits.slice(-10)}`);
  }

  return unique(keys.filter((key): key is string => key !== undefined));
};

/**
 * An address that reaches a role rather than a person. Two records sharing one
 * of these are two people who both answer `info@`, so it never merges them.
 */
export const isGenericEmail = (email: string | undefined): boolean => {
  const localPart = email?.split("@")[0];
  return (
    localPart !== undefined && GENERIC_EMAIL_LOCAL_PARTS.includes(localPart)
  );
};

const digitsOf = (value: unknown): string => {
  return (asText(value) ?? "").replace(/\D/g, "");
};

/** `00`, the international prefix most of the world dials. */
const hasInternationalPrefix = (digits: string): boolean => {
  return digits.startsWith("00") && digits.length > 4;
};

/** A national number kept with the trunk `0` its country dials it by. */
const hasTrunkPrefix = (digits: string): boolean => {
  return (
    digits.startsWith("0") && (digits.length === 10 || digits.length === 11)
  );
};

/** A NANP number, where the national number is the line itself. */
const isNorthAmerican = (digits: string): boolean => {
  return (
    (digits.length === 11 && digits.startsWith("1")) ||
    (digits.length === 10 && digits.startsWith("0") === false)
  );
};
