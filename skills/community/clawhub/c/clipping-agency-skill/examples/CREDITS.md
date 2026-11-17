# Credits for the example media

The two clients in `agency/` are made up, labelled EXAMPLE. Their episodes are short excerpts of two
Apollo 11 videos from the NASA Image and Video Library. Footage courtesy of NASA. This project is not
endorsed by NASA, and nobody who speaks or appears in the footage endorses anything here.

NASA's media guidelines: https://www.nasa.gov/nasa-brand-center/images-and-media/ (NASA material is
generally not subject to copyright in the United States; it may not be used to imply endorsement).

## Sources

| Example client | NASA video | File used | Bytes | SHA-256 of the file used |
|---|---|---|---|---|
| Example Mission Talks, ep-007 | Apollo 11 T-2 Day Press Conference, July 1969 (KSC), https://images.nasa.gov/details/KSC-19690715-MH-NAS01-0001-Historical_Video_Apollo_11_T-2_Day_Press_Conference-B_1493 | https://images-assets.nasa.gov/video/KSC-19690715-MH-NAS01-0001-Historical_Video_Apollo_11_T-2_Day_Press_Conference-B_1493/KSC-19690715-MH-NAS01-0001-Historical_Video_Apollo_11_T-2_Day_Press_Conference-B_1493~small.mp4 | 333,329,449 | 19fcebdfaee08db3d76ca4b5b58539cf3d41713f5fefa399f2b0f671bb22754d |
| Example Orbit Podcast, ep-012 | Apollo 11 20th Anniversary Crew Interviews, July 1989 (KSC), https://images.nasa.gov/details/KSC-19890701-MH-NAS01-0001-Apollo_11_20th_Anniversary_Crew_Interviews-B_2146 | https://images-assets.nasa.gov/video/KSC-19890701-MH-NAS01-0001-Apollo_11_20th_Anniversary_Crew_Interviews-B_2146/KSC-19890701-MH-NAS01-0001-Apollo_11_20th_Anniversary_Crew_Interviews-B_2146~small.mp4 | 769,394,559 | ddc6834c9a563cb25de1f9175f2e771c670c85376b043bc1ea760e85b607c35a |

Each episode's `source.mp4` is an excerpt of the file above, joined from these stretches (seconds
from the start of the NASA file), and is not in this repo:

- Mission Talks ep-007 (1969): 349.2 to 403.5, 695.2 to 709.0, 1426.0 to 1453.9.
- Orbit Podcast ep-012 (1989): 123.0 to 156.0, 549.0 to 589.5, 1214.7 to 1243.0.

The excerpts leave out the reporters asking questions and the 1989 moderator. The second 1989
stretch opens on a wide shot of the stage and the audience seen from behind (no faces); no clip
shows it, because Orbit clip 2 starts at the camera cut to the speaker. Only the Apollo 11 crew speak
or appear in the clips.

## The people in the footage

Only Apollo-era astronauts who no longer work for NASA appear, and the README never names them.

| Person | In the clips | Status, and the source |
|---|---|---|
| Neil Armstrong | speaks (Mission clip 1, Orbit clip 3) | died 25 August 2012: NASA biography, https://www.nasa.gov/wp-content/uploads/2016/01/armstrong_neil.pdf, and NASA JPL, https://www.jpl.nasa.gov/news/astronaut-neil-armstrong-1930-2012/ |
| Michael Collins | speaks (Mission clips 2 and 3, Orbit clips 1 and 2) | died 28 April 2021: NASA Johnson Space Center statement, https://www.nasa.gov/news-release/nasa-johnson-space-center-director-statement-on-the-passing-of-michael-collins/ |
| Buzz Aldrin | may be seen beside the others in wide shots; never quoted | resigned from NASA in July 1971: NASA biography, https://www.nasa.gov/wp-content/uploads/2016/01/aldrin_buzz.pdf |

## Media in this folder

Every file below was made by the skill's scripts from those excerpts, or drawn by a script:

- `agency/clients/*/episodes/*/clips/*.mp4`: the clips, cut by `make_clips.py` (360x640, small on
  purpose).
- `agency/clients/*/episodes/*/clips/*.jpg`: each clip's cover frame and the contact sheet, by
  `make_clips.py`.
- `agency/clients/*/brand/logo.png`: the made-up shows' logos, drawn with Pillow (plain shapes and
  text, no NASA insignia).
- `showcase.png`: page 1 of the Mission Talks approval page (`approve.py`), rendered at phone width
  (390 px) in headless Chrome.

The words on the clips come from a faster-whisper transcript of the footage. The shows, the handles
(`@example.orbit`, `@example.missiontalks`), the people named as approvers ("Alex Example", "Jordan
Example"), post ids, account ids and every number in the reports are made up.
