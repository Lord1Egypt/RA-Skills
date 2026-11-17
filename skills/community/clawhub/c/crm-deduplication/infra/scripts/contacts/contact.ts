// A CRM contact record, read into the person the rest of this path compares.

import { type CrmRecord, readCrmRecords } from "../common/records";
import { asNumber, asText } from "../common/values";
import {
  normalizeEmail,
  normalizeLinkedinProfile,
  normalizePhone,
  phoneMatchKeys,
} from "./identity";

/** A person, read from their CRM record. An absent value is `undefined`. */
export type Contact = {
  id: string;
  email: string | undefined;
  phone: string | undefined;
  /** Every form of this person's phone number another record could hold. */
  phoneKeys: string[];
  /** The LinkedIn profile as its handle: `jack-smith`. */
  linkedinUrl: string | undefined;
  linkedinPersonId: string | undefined;
  firstName: string | undefined;
  lastName: string | undefined;
  jobTitle: string | undefined;
  primaryAssociatedCompanyId: string | undefined;
  associatedDeals: number;
  activities: number;
  filledPropertyCount: number;
  createdAt: string;
  /** The stored email, for the review card: reviewers read what the CRM holds. */
  storedEmail: string | undefined;
};

/**
 * The contacts the searches returned, one per person. Both searches are passed
 * together because the second one re-returns records the first already found.
 */
export const readContacts = (...searchResults: unknown[]): Contact[] => {
  return readCrmRecords(...searchResults).map((record) => readContact(record));
};

const readContact = ({
  id,
  properties,
  filledPropertyCount,
}: CrmRecord): Contact => {
  return {
    id,
    email: normalizeEmail(properties.email),
    phone: normalizePhone(properties.phone),
    phoneKeys: phoneMatchKeys(properties.phone),
    linkedinUrl: normalizeLinkedinProfile(properties.linkedin_url),
    linkedinPersonId: asText(properties.linkedin_person_id),
    firstName: asText(properties.firstname),
    lastName: asText(properties.lastname),
    jobTitle: asText(properties.jobtitle),
    primaryAssociatedCompanyId: asText(properties.associatedcompanyid),
    associatedDeals: asNumber(properties.num_associated_deals),
    activities:
      asNumber(properties.hs_sales_email_last_replied) +
      asNumber(properties.num_contacted_notes),
    filledPropertyCount,
    createdAt: asText(properties.createdate) ?? "",
    storedEmail: asText(properties.email),
  };
};
