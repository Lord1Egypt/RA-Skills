export type Project = {
  id: string;
  title: string;
  createdAt?: string;
};

/** tRPC project initial data response */
export type ProjectInitialData = {
  project: Project;
  credits?: CreditsInfo;
};

export type CreditsInfo = {
  totalCredits?: number;
  usedCredits?: number;
  remainingCredits?: number;
};
