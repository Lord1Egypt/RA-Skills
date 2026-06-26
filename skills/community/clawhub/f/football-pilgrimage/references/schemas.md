# Response Schemas

## generate_pilgrimage

Returns a structured pilgrimage guide with emotional narrative, spot stories, On This Day events, and team crest:

```json
{
  "team": {
    "name": "AC Milan",
    "city": "Milan",
    "country": "Italy",
    "stadium": "San Siro",
    "founded": 1899,
    "colors": "Red & Black",
    "nickname": "I Rossoneri",
    "crest": "https://a.espncdn.com/i/teamlogos/soccer/500/103.png"
  },
  "on_this_day": [
    {
      "date": "04-15",
      "year": 2003,
      "event": "AC Milan defeated Ajax 3-2 in Champions League quarter-final",
      "significance": "Shevchenko scored a hat-trick to complete the comeback",
      "narrative_hook": "Did you know? On the day you depart, back in 2003, Shevchenko scored a hat-trick..."
    }
  ],
  "phases": [
    {
      "name": "Pre-departure — The Call",
      "crest_url": "https://...",
      "on_this_day_highlight": {"date": "04-15", "year": 2003, "event": "..."},
      "sections": [
        {"title": "Historic Echoes", "content": "..."},
        {"title": "Emotional Anchor", "content": "..."}
      ]
    },
    {
      "name": "Arrival Day — First Sight",
      "on_this_day_highlight": {"date": "04-16", "year": 2005, "event": "..."},
      "spots": [
        {
          "name": "Piazzale Angelo Moratti",
          "type": "landmark",
          "description": "The square named after the legendary Inter president",
          "address": "Piazzale Angelo Moratti, Milan",
          "story": "This square is named after Inter Milan's legendary president Angelo Moratti. In 1955, Moratti took over Inter...",
          "emotional_anchor": "Every fan who walks through here instinctively slows their pace"
        }
      ]
    },
    {
      "name": "Stadium Day — The Temple",
      "on_this_day_highlight": {"date": "04-17", "year": 2007, "event": "..."},
      "stadium_tour": {
        "name": "San Siro Tour",
        "booking_url": "...",
        "price": "€17",
        "hours": "9:30-17:00",
        "story": "San Siro was built in 1926, originally as AC Milan's home ground. In 1947, Inter Milan also moved in..."
      },
      "spots": [
        {
          "name": "San Siro Museum",
          "type": "museum",
          "description": "...",
          "address": "...",
          "story": "The museum's crown jewel is the match ball from the 2007 Champions League final...",
          "emotional_anchor": "Standing before that jersey, you can feel the weight of history"
        }
      ]
    },
    {
      "name": "Deep Experience — Immersion",
      "spots": []
    },
    {
      "name": "Departure — The Farewell",
      "sections": []
    }
  ],
  "trip_matches": {
    "matches_found": 1,
    "matches": [
      {
        "date": "2026-04-17",
        "competition": "La Liga",
        "opponent": "Atletico Madrid",
        "home_or_away": "home",
        "venue": "San Siro",
        "message": "🔥 Lucky you! On April 17, Milan will face... at San Siro!"
      }
    ],
    "itinerary_suggestion": "Schedule the stadium tour for April 16. Dedicate April 17 to the match day experience"
  },
  "travel_plan": {
    "flights": [],
    "hotels": []
  }
}
```

## get_stadium_info

```json
{
  "stadium": {
    "name": "San Siro",
    "official_name": "Stadio Giuseppe Meazza",
    "capacity": 75923,
    "address": "Piazzale Angelo Moratti, 20151 Milano MI, Italy",
    "opened": 1926,
    "tour_available": true,
    "tour_price": "€17",
    "tour_hours": "9:30-17:00",
    "museum": true,
    "story": "San Siro was built in 1926, funded by AC Milan president Piero Pirelli. Originally holding just 35,000, it has been expanded multiple times to its current 75,923 capacity. The stadium is officially named after legendary Italian player Giuseppe Meazza...",
    "legendary_moments": [
      "1965 European Cup Final: Inter Milan 1-0 Benfica",
      "May 2001: AC Milan celebrated their 17th league title here",
      "2016: Last Champions League final held here, Real Madrid beat Atletico on penalties"
    ]
  }
}
```

## get_pilgrimage_spots

Each spot now includes a **story** field with historical narrative:

```json
{
  "spots": [
    {
      "name": "Casa Milan Museum",
      "type": "museum",
      "description": "AC Milan official museum and headquarters",
      "address": "Via Aldo Rossi 8, Milan",
      "significance": "Club history, trophies, interactive exhibits",
      "story": "Casa Milan opened in 2014 as AC Milan's new headquarters and museum. Designed by architect Fabio Novembre, the building draws inspiration from Milan's red and black colors. It houses replicas of 7 Champions League trophies and precious memorabilia from legends like Maldini and Baresi...",
      "emotional_anchor": "Step inside and you'll understand why Milan fans say 'Milan is not just a club, it's a way of life'"
    },
    {
      "name": "Bar Sport San Siro",
      "type": "pub",
      "description": "Classic matchday gathering spot since 1978",
      "address": "Via Novara 2, near San Siro",
      "significance": "Pre-match atmosphere, local fans",
      "story": "This pub has witnessed countless match days at San Siro since opening in 1978. Owner Marco is a third-generation Milan fan, and the walls are covered with match tickets and signed photos dating back to the 1980s. Legend has it that Baresi himself came here for a drink after retiring...",
      "emotional_anchor": "Two hours before kickoff, fans spontaneously break into the club anthem here — it's a ritual that belongs to the fans"
    }
  ]
}
```

## get_on_this_day

Returns historic football events for **every day** of the user's trip, one event per day:

```json
{
  "team": "AC Milan",
  "departure_date": "2026-04-15",
  "duration": 5,
  "daily_events": [
    {
      "trip_day": 1,
      "calendar_date": "2026-04-15",
      "date_label": "04-15",
      "year": 2003,
      "event": "AC Milan defeated Ajax 3-2 in Champions League quarter-final second leg",
      "significance": "Shevchenko scored a hat-trick to complete the comeback after losing 0-1 in the first leg",
      "narrative_hook": "Did you know? On the day you depart, back in 2003, Shevchenko scored a hat-trick in Amsterdam, leading Milan's comeback against Ajax to reach the Champions League semi-finals.",
      "phase": "Pre-departure — The Call"
    },
    {
      "trip_day": 2,
      "calendar_date": "2026-04-16",
      "date_label": "04-16",
      "year": 2005,
      "event": "AC Milan signed Kaká from São Paulo FC",
      "significance": "The transfer that brought one of the greatest playmakers to San Siro",
      "narrative_hook": "Today is April 16. Back in 2005, Kaká officially joined AC Milan. From that moment, San Siro gained an angel.",
      "phase": "Arrival Day — First Sight"
    },
    {
      "trip_day": 3,
      "calendar_date": "2026-04-17",
      "date_label": "04-17",
      "year": 1994,
      "event": "AC Milan 3-0 Monaco in Champions League semi-final",
      "significance": "A dominant display that paved the way to the 1994 Champions League title",
      "narrative_hook": "Today is April 17. Back in 1994, Milan swept Monaco 3-0 in the Champions League semi-final. That Capello-coached Milan side was one of the greatest teams in football history.",
      "phase": "Stadium Day — The Temple"
    },
    {
      "trip_day": 4,
      "calendar_date": "2026-04-18",
      "date_label": "04-18",
      "year": 2010,
      "event": "Ronaldinho scored a stunning free-kick against Juventus at San Siro",
      "significance": "One of the most memorable goals in the Milan derby era",
      "narrative_hook": "Today is April 18. Back in 2010, Ronaldinho stunned Juventus with a breathtaking free-kick at San Siro.",
      "phase": "Deep Experience — Immersion"
    },
    {
      "trip_day": 5,
      "calendar_date": "2026-04-19",
      "date_label": "04-19",
      "year": 2007,
      "event": "AC Milan defeated Manchester United 3-0 in Champions League semi-final",
      "significance": "Kaká's masterclass performance — two goals that stunned Old Trafford",
      "narrative_hook": "On the day you leave, back in 2007, Kaká delivered one of the greatest individual performances in Champions League history at Old Trafford. Carrying this memory as you depart is the perfect farewell.",
      "phase": "Departure — The Farewell"
    }
  ]
}
```

## get_trip_matches

Returns matches found during the user's trip dates:

```json
{
  "team": "Barcelona",
  "trip_start": "2026-04-15",
  "trip_end": "2026-04-19",
  "matches_found": 1,
  "matches": [
    {
      "date": "2026-04-18",
      "kickoff_time": "21:00 CEST",
      "competition": "La Liga",
      "opponent": {
        "name": "Real Sociedad",
        "crest": "https://a.espncdn.com/i/teamlogos/soccer/500/89.png"
      },
      "venue": {
        "name": "Spotify Camp Nou",
        "city": "Barcelona"
      },
      "home_or_away": "home",
      "status": "not_started",
      "is_highlight": true,
      "message": "🔥 Lucky you! On Day 4 of your trip (April 18), Barcelona will face Real Sociedad at Camp Nou! This is your chance to witness a match at the sacred ground!",
      "ticket_tips": "Book tickets in advance via Barcelona's official website (fcbarcelona.com). Recommended: Gol Nord stand (ultras section), tickets approx. €50-150"
    }
  ],
  "itinerary_suggestion": "Schedule the stadium tour for April 17 (day before the match). Dedicate April 18 to the match day experience: pre-match pub → photos outside the stadium → enter and watch → post-match celebration"
}
```

When no matches are found:

```json
{
  "team": "Barcelona",
  "trip_start": "2026-04-15",
  "trip_end": "2026-04-19",
  "matches_found": 0,
  "matches": [],
  "message": "😢 No Barcelona matches scheduled during your trip, but the Camp Nou tour and museum are equally stunning! Check the schedule again before departure — league fixtures may be rescheduled."
}
```

## get_travel_plan

```json
{
  "flights": [
    {
      "flight_no": "MU...",
      "departure": "Shanghai",
      "arrival": "Milan",
      "price": "¥...",
      "jump_url": "..."
    }
  ],
  "hotels": [
    {
      "name": "...",
      "star": "...",
      "price": "...",
      "jump_url": "..."
    }
  ]
}
```
