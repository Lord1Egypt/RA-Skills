import numpy as np
#Cos相似性
def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2)
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return dot / norm_product if norm_product != 0 else 0.0
#遍历
def build_similarity_matrix(vectors):
    n = len(vectors)
    sim_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            sim_matrix[i, j] = cosine_similarity(vectors[i], vectors[j])
    return sim_matrix
#提取
def get_top_n_values(array, n):
    top_indices = np.argsort(array)[-n:][::-1]
    top_values = array[top_indices]
return top_values, top_indices