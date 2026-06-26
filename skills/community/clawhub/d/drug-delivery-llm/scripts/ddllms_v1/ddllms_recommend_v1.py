import numpy as np
import networkx as nx
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
class SMILESProcessor:
    def __init__(self, paths):
        self.paths = paths
        self.raw_data = []
        self.processed_data = []
    def load_data(self):
        for path in self.paths:
            smiles = np.load(path)
            self.raw_data.append(smiles)
    def process_data(self, postprocess_fn):
        self.processed_data = [postprocess_fn(smiles) for smiles in self.raw_data]
        return self.get_combined_unique()
    def get_combined_unique(self):
        all_smiles = np.concatenate(self.processed_data, axis=0)
        return get_uni_str(all_smiles)
class FeatureEngineer:
    def __init__(self, fingerprint_sets, extra_features=None):
        """
        fingerprint_sets: list of np.arrays with shape [N, D]
        extra_features: list of (N, 1) arrays like SA, QED, etc.
        """
        self.fingerprint_sets = fingerprint_sets
        self.extra_features = extra_features or []
    def combine_features(self):
        combined = []
        for fp in self.fingerprint_sets:
            combined.append(fp)
        if self.extra_features:
            extra = np.concatenate(self.extra_features, axis=1)
            combined.append(extra)
        return np.concatenate(combined, axis=0)
    def reduce_dimensionality(self, vectors, n_components=20):
        self.pca = PCA(n_components=n_components)
        return self.pca.fit_transform(vectors)
    def tsne_embed(self, vectors, **kwargs):
        tsne = TSNE(n_components=2, init='pca', method='exact', angle=1.0,
                    early_exaggeration=5, n_iter=1000, min_grad_norm=1e-3, **kwargs)
        return tsne.fit_transform(vectors)
class SimilarityGraph:
    @staticmethod
    def cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def __init__(self, vectors):
        self.vectors = vectors
    def build_graph(self):
        n = len(self.vectors)
        adjacency_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                adjacency_matrix[i, j] = self.cosine_similarity(self.vectors[i], self.vectors[j])
        self.graph = nx.from_numpy_array(adjacency_matrix)
        return self.graph
    def run_pagerank(self, alpha=0.5, top_k=40):
        scores = nx.pagerank(self.graph, alpha=alpha, max_iter=600, tol=1e-3)
        sorted_nodes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [node for node, _ in sorted_nodes[:top_k]]
def main():
    # === Step 1: 数据 ===
    paths = [
        "YOUR_PATH/YourNPYdata.npy",  # baseline
        "YOUR_PATH/YourNPYdata.npy",  # gemma
        "YOUR_PATH/YourNPYdata.npy"   # neox
    ]
    smiles_proc = SMILESProcessor(paths)
    smiles_proc.load_data()
    unique_smiles = smiles_proc.process_data(post_smi)
    # === Step 2: 预处理===
    fingerprints_baseline = fingerprint_baseline   # shape [N1, D]
    fingerprints_gemma = fingerprint_gemma         # shape [N2, D]
    fingerprints_neox = fingerprint_neox           # shape [N3, D]
    sa_gemma = synthetic_accessibility_gemma.reshape(-1, 1)
    qed_gemma = qed_score_gemma.reshape(-1, 1)
    feature_engineer = FeatureEngineer(
        fingerprint_sets=[fingerprints_baseline, fingerprints_gemma, fingerprints_neox],
        extra_features=[sa_gemma, qed_gemma]
    )
    combined_features = feature_engineer.combine_features()
    reduced_features = feature_engineer.reduce_dimensionality(fingerprints_baseline)
    tsne_vectors = feature_engineer.tsne_embed(combined_features)
    # === Step 3: PageRank===
    sim_graph = SimilarityGraph(tsne_vectors)
    graph = sim_graph.build_graph()
    top_nodes = sim_graph.run_pagerank(top_k=40)
    print("Top 40 recommendations:", top_nodes)
if __name__ == "__main__":
    main()