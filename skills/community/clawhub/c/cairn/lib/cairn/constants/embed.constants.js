// Vector length is pinned per embed model — must match what the model returns
// AND the schema's `chunks_vec`/`entities_vec` column declaration.
export const DIM_BY_MODEL = {
    'nomic-embed-text': 768,
};
