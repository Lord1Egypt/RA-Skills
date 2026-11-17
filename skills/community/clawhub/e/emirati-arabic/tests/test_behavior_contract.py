"""Instruction-presence checks only; not a conversation or fluency test."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BehaviorContractTests(unittest.TestCase):
    def assert_contract_guidance(self, heading, skill_fragments, reference_fragments):
        """Guard editorial instruction presence, not generated behavior or fluency."""
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        contract = text.split('## Conversation and writing contract', 1)[1].split('\n## ', 1)[0]
        rules = [line for line in contract.splitlines() if '**' + heading + '**' in line]
        self.assertEqual(len(rules), 1, 'Expected one loaded rule: ' + heading)
        for fragment in skill_fragments:
            with self.subTest(skill_fragment=fragment):
                self.assertIn(fragment, rules[0])
        reference = (ROOT / 'references/conversation-behavior.md').read_text(encoding='utf-8')
        for fragment in reference_fragments:
            with self.subTest(reference_fragment=fragment):
                self.assertIn(fragment, reference)

    def test_speakable_collocations_take_priority_over_dialect_display(self):
        self.assert_contract_guidance(
            'Compose, do not substitute.',
            ('ordinary speakable sentence', 'collocations', 'clear shared wording',
             'forcing dialect markers'),
            ('تراكيب مألوفة قابلة للقول', 'صياغة واضحة مشتركة'))

    def test_self_directed_humor_has_an_explicit_grounded_target(self):
        self.assert_contract_guidance(
            'Make self-directed humor legible.',
            ("speaker's stated action or mishap", 'implied sarcasm', 'boasting',
             'Do not invent a mishap'),
            ('الفعل أو الموقف الذي ذكره المتكلم', 'سخرية ضمنية', 'مدح النفس'))

    def test_practical_drafts_do_not_invent_private_states_for_politeness(self):
        self.assert_contract_guidance(
            'Ground practical drafts in supplied facts.',
            ('first-person', 'speaker or addressee', 'feelings, motives, knowledge, or excuses',
             'politeness', 'draft label'),
            ('مشاعر أو دوافع أو معرفة أو أعذار', 'للمتكلم أو المخاطَب',
             'لمجرد تلطيف الرسالة', 'تسمية النص مسودة'))

    def test_grounding_allows_warmth_proposals_and_requested_fiction(self):
        self.assert_contract_guidance(
            'Ground practical drafts in supplied facts.',
            ('observable action supplied', 'proposals as proposals',
             'not established facts or agreements', 'Fiction is allowed when explicitly requested'),
            ('فعل ظاهر ورد في السياق', 'الاقتراح بوصفه اقتراحًا',
             'لا حقيقة أو اتفاقًا قائمًا', 'التخييل مسموح إذا طُلب صراحة'))

    def test_temporary_english_artifact_returns_to_prior_dialogue_dialect(self):
        self.assert_contract_guidance(
            'Honor language and register changes.',
            ('resume the previously selected dialogue dialect',
             'unless the user changes the ongoing conversation language'),
            ('ارجع بعدها إلى لهجة الحوار المختارة سابقًا',
             'ما لم يطلب المستخدم تغيير لغة المحادثة المستمرة'))

    def test_user_correction_replaces_only_the_affected_assumption(self):
        self.assert_contract_guidance(
            'Apply corrections locally.',
            ('user correction overrides your erroneous assumption',
             'affected context', 'Do not extrapolate',
             'unrelated facts, future situations, or a universal dialect rule'),
            ('تصحيح المستخدم يتقدّم على افتراضك الخاطئ',
             'في السياق المتأثر فقط', 'لا تستنتج منه حقائق أخرى'))

    def test_spoken_scripts_keep_actor_action_and_referent_clear(self):
        """Guard general clarity instructions, not a preferred script or word ban."""
        self.assert_contract_guidance(
            'Keep spoken-script references clear.',
            ('voiceover or dialogue', 'who acts, what happens, and which person or object',
             'explicit noun', 'pronoun', 'kinship term', 'body-part spelling',
             'Do not silently choose between materially different actions',
             'not a global ban on a dialect word', 'Preserve protected quotations'),
            ('من يفعل ماذا', 'الشخص أو الشيء المقصود', 'اسمًا صريحًا',
             'ضمير', 'لفظ قرابة', 'رسم عضو من الجسم',
             'لا تحسم بين فعلين مختلفين', 'ليس منعًا عامًا لكلمة لهجية',
             'احفظ الاقتباسات المحمية'))

    def test_shared_kinship_body_part_form_requires_distinct_spoken_references(self):
        """Guard contextual disambiguation instructions, not a generated answer."""
        self.assert_contract_guidance(
            'Keep spoken-script references clear.',
            ('kinship term and a body part share an ambiguous written form in the same scene',
             'unambiguous relationship, role, or name for the person',
             'explicit body-part noun for the hand',
             'Do not rely only on poetic adjectives, diacritics, or surrounding warmth',
             'Re-read the whole script as spoken text',
             'replace any remaining ambiguous reference',
             'not a global ban on a dialect word', 'Preserve protected quotations'),
            ('إذا اشترك لفظ القرابة وعضو من الجسم في رسم ملتبس داخل المشهد نفسه',
             'صلة قرابة أو دور أو اسم لا يلتبس', 'اسم صريح لعضو الجسم عند ذكر اليد',
             'لا تعتمد فقط على الصفات الشعرية أو التشكيل أو دفء السياق',
             'أعد قراءة النص كله بوصفه كلامًا منطوقًا', 'استبدل كل إحالة ما زالت ملتبسة',
             'ليس منعًا عامًا لكلمة لهجية', 'احفظ الاقتباسات المحمية'))

    def test_intent_first_contract_is_in_loaded_skill(self):
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('description: Converse and write in Emirati; Abu Dhabi on request.', text)
        for metadata in ('version: 0.2.1-rc.1',
                         'behavior_revision: intent-first-rc-1'):
            with self.subTest(metadata=metadata):
                self.assertIn(metadata, text.splitlines())
        self.assertIn('## Conversation and writing contract', text)
        contract = text.split('## Conversation and writing contract', 1)[1].split('\n## ', 1)[0]
        for rule in ('Do the original task', 'Respond to contextual intent',
                     'Produce the requested response', 'Compose, do not substitute',
                     'Do not invent personal experience', 'Choose an appropriate action',
                     'Clarify only consequential ambiguity', 'Generalize the method',
                     'Honor language and register changes'):
            with self.subTest(rule=rule):
                self.assertIn(rule, contract)
        self.assertIn('references/conversation-behavior.md', text)
        self.assertTrue((ROOT / 'references/conversation-behavior.md').is_file())

    def test_dateless_illustrative_drafts_do_not_add_today(self):
        """Check example/context consistency only, not dialect fluency."""
        text = (ROOT / 'references/conversation-behavior.md').read_text(encoding='utf-8')
        cases = (
            ('إنجاز طلب كتابة',
             '- الطلب التوضيحي: «سرت العين وعقب دبي ورديت بوظبي. اكتب لي رسالة قصيرة أقول فيها لربيعي إني تعبت من المشاوير.»',
             '- مسودة مقترحة للمستخدم: '),
            ('الرد على كلام منقول',
             '- السياق التوضيحي: تنقل المستخدم بين العين ودبي وبوظبي، وقال له صاحبه: «اسميك ضربت خطوط»؛ طلب المستخدم ردًا خفيفًا.',
             '- مسودة مقترحة: '),
        )
        for heading, context, draft_prefix in cases:
            with self.subTest(heading=heading):
                section = text.split('### ' + heading + '\n', 1)[1].split('\n### ', 1)[0]
                self.assertIn(context, section)
                drafts = [line.removeprefix(draft_prefix) for line in section.splitlines()
                          if line.startswith(draft_prefix)]
                self.assertEqual(len(drafts), 1)
                self.assertNotIn('اليوم', drafts[0],
                                 'The dateless context does not establish today.')

    def test_regional_reference_does_not_require_dictionary_first(self):
        text = (ROOT / 'references/abu-dhabi.md').read_text(encoding='utf-8')
        self.assertNotIn('اقرأ [المعجم المنظّم](abu-dhabi-lexicon.json) ثم', text)
        self.assertIn('conversation-behavior.md', text)
        self.assertIn('المحادثة الحالية', text)


if __name__ == '__main__':
    unittest.main()
