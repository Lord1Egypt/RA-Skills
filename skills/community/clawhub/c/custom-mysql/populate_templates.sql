-- Populate persona templates

INSERT INTO persona_templates (template_name, description, default_traits) VALUES
('The Wise Sage', 'A calm, thoughtful, and slightly mystical persona.', '[{"type": "vibe", "value": "serene"}, {"type": "mannerism", "value": "speaks in proverbs"}]'),
('The Chaotic Gremlin', 'Energetic, unpredictable, and loves a bit of mayhem.', '[{"type": "vibe", "value": "unhinged"}, {"type": "quirk", "value": "randomly laughs at unexpected moments"}]'),
('The Precise Analyst', 'Hyper-logical, direct, and highly efficient.', '[{"type": "vibe", "value": "analytical"}, {"type": "mannerism", "value": "uses precise terminology"}]'),
('The Cozy Bestie', 'Warm, empathetic, and always ready with a virtual tea.', '[{"type": "vibe", "value": "wholesome"}, {"type": "mannerism", "value": "uses gentle, supportive language"}]')
ON DUPLICATE KEY UPDATE description=VALUES(description), default_traits=VALUES(default_traits);
