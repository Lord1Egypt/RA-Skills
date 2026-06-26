import type { SubmissionProfile } from "@caixu/contracts";

export const submissionProfiles: Record<string, SubmissionProfile> = {
  judge_demo_v1: {
    profile_id: "judge_demo_v1",
    target_url:
      process.env.CAIXU_JUDGE_DEMO_URL ?? "http://127.0.0.1:3000/judge-demo",
    file_fields: ["materials_zip"],
    text_fields: {
      applicant_name: "Demo Student",
      target_goal: "summer_internship_application"
    },
    success_text: ["Submission received", "提交成功"],
    screenshot_steps: ["open_form", "upload_package", "submit_result"],
    log_sampling: "normal"
  }
};

export function getSubmissionProfile(profileId: string): SubmissionProfile {
  const profile = submissionProfiles[profileId];
  if (!profile) {
    throw new Error(`Unsupported submission profile: ${profileId}`);
  }
  return profile;
}
