import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('planner', ROOT / 'scripts/next_tasks.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / 'examples/plan.json').read_text())

    def external(self):
        t = self.plan['tasks'][1]
        t.update(external_write=True, effect_key='single-business-action')
        return t

    def test_ready_only_after_dependencies(self):
        out = mod.inspect(self.plan)
        self.assertEqual(out['ready'], ['vendor-b']); self.assertFalse(out['merge_ready'])

    def test_cycle(self):
        self.plan['tasks'][1]['depends_on'] = ['comparison']
        with self.assertRaisesRegex(ValueError, 'cycle'): mod.inspect(self.plan)

    def test_unknown_dependency(self):
        self.plan['tasks'][1]['depends_on'] = ['missing']
        with self.assertRaisesRegex(ValueError, 'unknown'): mod.inspect(self.plan)

    def test_uncertain_cannot_be_retried(self):
        self.external().update(status='uncertain', retry_decision='approved', authorization_ref='user-msg')
        self.assertEqual(mod.inspect(self.plan)['ready'], [])

    def test_failed_external_cannot_be_retried(self):
        self.external().update(status='failed', retry_decision='approved', authorization_ref='user-msg')
        self.assertEqual(mod.inspect(self.plan)['ready'], [])

    def test_failed_read_only_needs_decision(self):
        self.plan['tasks'][1]['status'] = 'failed'
        self.assertEqual(mod.inspect(self.plan)['ready'], [])
        self.plan['tasks'][1]['retry_decision'] = 'approved'
        self.assertEqual(mod.inspect(self.plan)['ready'], ['vendor-b'])

    def test_external_requires_authorization(self):
        t = self.external(); self.assertEqual(mod.inspect(self.plan)['ready'], [])
        t['authorization_ref'] = 'user-message-1'
        self.assertEqual(mod.inspect(self.plan)['ready'], ['vendor-b'])

    def test_budget_combines_ready_nodes(self):
        self.plan['budget']['limit'] = 12
        other = copy.deepcopy(self.plan['tasks'][1]); other['id'] = 'vendor-c'
        self.plan['tasks'].append(other)
        self.assertEqual(mod.inspect(self.plan)['ready'], ['vendor-b'])

    def test_running_budget_is_reserved(self):
        self.plan['tasks'][1]['status'] = 'running'
        with self.assertRaisesRegex(ValueError, 'reservations'): mod.inspect(self.plan)

    def test_evidence_required(self):
        del self.plan['tasks'][0]['evidence_ref']
        with self.assertRaisesRegex(ValueError, 'evidence_ref'): mod.inspect(self.plan)

    def test_repeated_external_effect_rejected(self):
        t = self.external(); other = copy.deepcopy(t); other['id'] = 'repeat'
        self.plan['tasks'].append(other)
        with self.assertRaisesRegex(ValueError, 'business action'): mod.inspect(self.plan)

    def test_accepted_external_needs_receipt(self):
        self.external().update(status='accepted', evidence_ref='artifact')
        with self.assertRaisesRegex(ValueError, 'receipt_ref'): mod.inspect(self.plan)

    def test_all_accepted_allows_merge_without_claiming_verification(self):
        for t in self.plan['tasks']: t.update(status='accepted', evidence_ref='example-evidence')
        result = mod.inspect(self.plan)
        self.assertTrue(result['merge_ready']); self.assertFalse(result['evidence_verified'])

    def test_invalid_budget(self):
        for value in [True, -1, float('nan'), float('inf')]:
            self.plan['budget']['limit'] = value
            with self.assertRaises(ValueError): mod.inspect(self.plan)
