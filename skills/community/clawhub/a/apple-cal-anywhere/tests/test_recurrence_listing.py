import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "applecal.py"
spec = importlib.util.spec_from_file_location("applecal", MODULE_PATH)
applecal = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(applecal)


class RecurrenceListingTests(unittest.TestCase):
    def test_parse_ics_event_honors_tzid_for_expanded_instance(self):
        ics = """BEGIN:VCALENDAR
BEGIN:VEVENT
UID:AA2E2923-C25B-43AD-A407-25C2B58EB35D
SUMMARY:Tennis Class
DTSTART;TZID=Australia/Melbourne:20260330T163000
DTEND;TZID=Australia/Melbourne:20260330T170000
RECURRENCE-ID:20260330T053000Z
END:VEVENT
END:VCALENDAR
"""

        event = applecal.parse_ics_event(ics)

        self.assertEqual(event["start"], "2026-03-30T05:30:00+00:00")
        self.assertEqual(event["end"], "2026-03-30T06:00:00+00:00")
        self.assertEqual(event["summary"], "Tennis Class")

    def test_list_events_requests_expand_and_returns_expanded_occurrence(self):
        response_xml = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
<d:multistatus xmlns:d=\"DAV:\" xmlns:c=\"urn:ietf:params:xml:ns:caldav\">
  <d:response>
    <d:href>/cal/AA2E2923-C25B-43AD-A407-25C2B58EB35D.ics</d:href>
    <d:propstat>
      <d:prop>
        <c:calendar-data>BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:AA2E2923-C25B-43AD-A407-25C2B58EB35D\nSUMMARY:Tennis Class\nDTSTART;TZID=Australia/Melbourne:20260330T163000\nDTEND;TZID=Australia/Melbourne:20260330T170000\nRECURRENCE-ID:20260330T053000Z\nEND:VEVENT\nEND:VCALENDAR\n</c:calendar-data>
      </d:prop>
      <d:status>HTTP/1.1 200 OK</d:status>
    </d:propstat>
  </d:response>
</d:multistatus>
"""

        class FakeResponse:
            status_code = 207
            text = response_xml

            def raise_for_status(self):
                return None

        captured = {}

        def fake_request(method, url, **kwargs):
            captured["method"] = method
            captured["url"] = url
            captured["data"] = kwargs.get("data", "")
            return FakeResponse()

        client = applecal.AppleCalClient.__new__(applecal.AppleCalClient)
        client._request = fake_request

        events = client.list_events(
            "https://caldav.icloud.com/family/",
            "2026-03-30T00:00:00+11:00",
            "2026-03-30T23:59:59+11:00",
            query="Tennis",
        )

        self.assertEqual(captured["method"], "REPORT")
        self.assertIn("<c:expand", captured["data"])
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["start"], "2026-03-30T05:30:00+00:00")
        self.assertEqual(events[0]["end"], "2026-03-30T06:00:00+00:00")

    def test_non_recurring_utc_event_parsing_still_works(self):
        ics = """BEGIN:VCALENDAR
BEGIN:VEVENT
UID:ONE-OFF-123
SUMMARY:Dentist
DTSTART:20260330T010000Z
DTEND:20260330T013000Z
END:VEVENT
END:VCALENDAR
"""

        event = applecal.parse_ics_event(ics)

        self.assertEqual(event["start"], "2026-03-30T01:00:00+00:00")
        self.assertEqual(event["end"], "2026-03-30T01:30:00+00:00")
        self.assertFalse(event["all_day"])


if __name__ == "__main__":
    unittest.main()
